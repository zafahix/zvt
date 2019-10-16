# -*- coding: utf-8 -*-

import pandas as pd

from zvdata.utils.pd_utils import df_is_not_null, fill_with_same_index, normal_index_df


class NormalData(object):
    table_type_sample = None

    def __init__(self,
                 df,
                 annotation_df=None,
                 category_field='entity_id',
                 index_field='timestamp',
                 fill_index: bool = False) -> None:
        self.data_df = df
        self.annotation_df: pd.DataFrame = annotation_df
        self.category_field = category_field
        self.index_field = index_field
        self.fill_index = fill_index

        self.entity_ids = []
        self.df_list = []
        self.entity_map_df = {}

        self.normalize()

    def is_normalized(self):
        if df_is_not_null(self.data_df):
            names = self.data_df.index.names

            if len(names) == 2 and names[0] == self.category_field and names[1] == self.index_field:
                return True

        return False

    def normalize(self):
        """
        normalize data_df to
                                    col1    col2    col3
        entity_id    index_field

        """
        if df_is_not_null(self.data_df):
            if not self.is_normalized():
                self.data_df = normal_index_df(self.data_df)

            self.entity_ids = self.data_df.index.levels[0].to_list()

            for entity_id in self.entity_ids:
                df = self.data_df.loc[(entity_id,)]
                self.df_list.append(df)
                self.entity_map_df[entity_id] = df

            if len(self.df_list) > 1 and self.fill_index:
                self.df_list = fill_with_same_index(df_list=self.df_list)

    def empty(self):
        return not df_is_not_null(self.data_df)
