from typing import List
import numpy as np
from models.Point import Point


class PostCluster:
    
    def __init__(self, central_point, points):
        # Social
        self._name = ''
        self._category_name = ""
        self._category = -2
        self._texts = []
        self._tags = []
        self.descr = ''
        self.image_url = ''
        # Stat
        self._tags_relevance_stat = []
        self._tags_sentiment_stat = []
        self._texts_relevance_stat = []
        self._texts_sentiment_stat = []
        # Marks
        self._mark = -2
        self._system_mark = -2
        self._users_marks = []
        # Geo
        self._central_point = central_point
        self._geo_points = points
    
    def set_texts(self, texts):
        self._texts = texts
    
    def set_tags(self, tags):
        self._tags = tags
    
    def set_points(self, points: List[Point]):
        self._geo_points = points
    
    def set_system_mark(self, mark: float):
        self._system_mark = mark
        if self._mark < 0:
            self._mark = mark
    
    def set_category(self, category: int):
        self._category = category
    
    def set_tags_relevance_stat(self, relevance_mask, relevance_stat):
        self._tags_relevance_stat = relevance_stat
        self._delete_points(relevance_mask)
    
    def set_tags_sentiment_stat(self, sentiment_stat):
        self._tags_sentiment_stat = sentiment_stat
    
    def set_texts_relevance_stat(self, relevance_mask, relevance_stat):
        self._texts_relevance_stat = relevance_stat
        self._delete_points(relevance_mask)
    
    def set_texts_sentiment_stat(self, sentiment_stat):
        self._texts_sentiment_stat = sentiment_stat
    
    def set_posts(self, sm_points):
        texts = []
        tags = []
        points = []
        for point in sm_points:
            texts.append(point.get_text())
            tags.append(point.get_tags())
            points.append(point.get_point())
        self._texts = texts
        self._tags = tags
        self._geo_points = points
    
    def get_texts(self):
        return self._texts
    
    def get_tags(self):
        return self._tags
    
    def get_points(self):
        return self._geo_points
    
    def get_central_point(self):
        return self._central_point
    
    def get_system_mark(self):
        return self._system_mark
    
    def get_category(self):
        return self._category
    
    def get_tags_relevance(self):
        return self._tags_relevance_stat
    
    def get_tags_sentiment(self):
        return self._tags_sentiment_stat
    
    def get_texts_relevance(self):
        return self._texts_relevance_stat
    
    def get_texts_sentiment(self):
        return self._texts_sentiment_stat
    
    def set_name(self, param):
        self._name = param
    
    def get_name(self):
        return self._name
    
    def set_user_mark(self, mark):
        self._users_marks.append(mark)
    
    def get_users_marks(self):
        return self._users_marks
    
    def get_mark(self):
        if self._mark < 0:
            return self._system_mark
        return self._mark
    
    def set_mark(self, mark):
        self._mark = mark
    
    def set_category_name(self, category_name):
        self._category_name = category_name
        
    def get_category_name(self):
        return self._category_name
    
    def size(self):
        return len(self._geo_points)
    
    def _delete_points(self, mask):
        self._texts = self._delete(self._texts, mask)
        self._tags = self._delete(self._tags, mask)
        self._geo_points = self._delete(self._geo_points, mask)
        
        if len(self._tags_sentiment_stat) > 0:
            self._tags_sentiment_stat = self._delete(self._tags_sentiment_stat, mask)
        self._tags_relevance_stat = self._delete(self._tags_relevance_stat, mask)
        if len(self._texts_sentiment_stat) > 0:
            self._texts_sentiment_stat = self._delete(self._texts_sentiment_stat, mask)
        if len(self._texts_relevance_stat) > 0:
            self._texts_relevance_stat = self._delete(self._texts_relevance_stat, mask)
    
    def _delete(self, arr, mask):
        return np.array(arr)[mask]
