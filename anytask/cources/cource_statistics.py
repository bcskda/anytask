from django.db.models import Q

from tasks.models import TaskTaken

class CourceStatistics(object):
    
    def __init__(self, cource_tasks):
        self.cource_tasks = cource_tasks
        self.groups_statistics = {}
        self.cource_statistics = {
            'summ_scores' : 0,
            'number_students' : 0,
            'number_students_with_tasks' : 0,
            'middle_score' : 0,
            'middle_score_on_students' : 0,
            'ratio' : 0,        
        } 
        
    def update(self, group):
        self.add_statistics_for_group(group)
        self.update_cource_statistics(group)
        
    def get_cource_statistics(self):
        (self.cource_statistics['middle_score'], self.cource_statistics['middle_score_on_students'], self.cource_statistics['ratio']) = self._calculate_scores_statistics(self.cource_statistics['number_students'], 
                                                                                                                                              self.cource_statistics['number_students_with_tasks'], 
                                                                                                                                              self.cource_statistics['summ_scores'])
       
        groups_statistics_list = []
        for group,statistics in self.groups_statistics.iteritems():
            groups_statistics_list.append((group, statistics['group_summ_scores'], 
                                                  statistics['number_group_students'],
                                                  statistics['number_students_with_tasks'],
                                                  statistics['middle_score'],
                                                  statistics['middle_score_on_group'],
                                                  statistics['ratio']))
        
        groups_statistics_list.append((None, self.cource_statistics['summ_scores'],
                                            self.cource_statistics['number_students'],
                                            self.cource_statistics['number_students_with_tasks'],
                                            self.cource_statistics['middle_score'],
                                            self.cource_statistics['middle_score_on_students'],
                                            self.cource_statistics['ratio'])) 
        
        return groups_statistics_list
    
    def get_groups_statistics(self):
        group_student_list = []
        
        for group,statistics in self.groups_statistics.iteritems():
            group_student_list.append((group, statistics['students_statistics']))
            
        return group_student_list
    
    def add_statistics_for_group(self, group):
        statistics = {
            'group_summ_scores' : 0,
            'number_group_students' : 0,
            'number_students_with_tasks' : 0,
            'middle_score' : 0,
            'middle_score_on_group' : 0,
            'ratio' : 0,
            'students_statistics' : [],          
        } 
        
        group_students = []
        statistics['number_group_students'] = group.students.count()
        
        for student in group.students.filter(is_active=True).order_by('last_name', 'first_name'):
            task_takens = TaskTaken.objects.filter(user = student).filter(task__in=self.cource_tasks).filter(Q( Q(status=TaskTaken.STATUS_TAKEN) | Q(status=TaskTaken.STATUS_SCORED)))
            statistics['number_students_with_tasks'] += 0 if task_takens.count() == 0 else 1

            (scores, student_tasks_list) = self._get_student_statistics(task_takens)
            
            group_students.append((student, scores, student_tasks_list))
            statistics['group_summ_scores'] += scores
        
        statistics['students_statistics'] = group_students
        (statistics['middle_score'], statistics['middle_score_on_group'], statistics['ratio']) = self._calculate_scores_statistics(statistics['number_group_students'], 
                                                                                                           statistics['number_students_with_tasks'], 
                                                                                                           statistics['group_summ_scores'])
        
        self.groups_statistics[group] = statistics
    
    def update_cource_statistics(self, group):
        group_statistics = self.groups_statistics[group]
        
        self.cource_statistics['summ_scores'] += group_statistics['group_summ_scores']
        self.cource_statistics['number_students'] += group_statistics['number_group_students']
        self.cource_statistics['number_students_with_tasks'] += group_statistics['number_students_with_tasks']
    
    def _get_student_statistics(self, student_task_takens):
        scores = 0
        student_tasks_list = []
        
        for task_taken in student_task_takens:
            scores += task_taken.score
            student_tasks_list.append((task_taken.task, task_taken.score))
        
        return (scores, student_tasks_list)
    
    def _calculate_scores_statistics(self, number_of_students, number_of_students_with_tasks, scores):
        if number_of_students == 0 or number_of_students_with_tasks == 0:
            return (0,0,0)
        return (float(scores)/number_of_students_with_tasks, float(scores)/number_of_students, float(number_of_students_with_tasks)/number_of_students)
        
        
        