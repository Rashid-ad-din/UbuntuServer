from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from cabinet_parents.models import Survey
from cabinet_parents.models import Survey, City, StudentArea, TutorArea
from cabinet_parents.models import Subject
from cabinet_tutors.models import TutorCabinets, SubjectsAndCosts, Education
from reviews.models import Review


class BoardStudentView(ListView):
    template_name = 'board_student.html'
    model = Survey
    context_object_name = 'surveys'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['subjects'] = Subject.objects.all()
        context['cities'] = City.objects.all()
        return context


class FilterStudentView(ListView):
    template_name = 'board_student.html'
    model = Survey
    context_object_name = 'surveys'

    def get(self, request, *args, **kwargs):
        self.min_cost = request.GET.get("min_cost")
        self.max_cost = request.GET.get("max_cost")
        self.subject = request.GET.get("subject")
        self.city = request.GET.get("city")
        self.format = request.GET.get("format")
        self.order = request.GET.get("order")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        surveys = Survey.objects.all()
        print(self.format)
        context = super().get_context_data(object_list=None, **kwargs)
        if self.city and self.format == "student":
            studentArea = StudentArea.objects.filter(student_city_id=self.city)
            surveys = Survey.objects.filter(student_area__in=studentArea)
        if self.city and self.format == "tutor":
            tutorArea = TutorArea.objects.filter(tutor_city_id=self.city)
            surveys = Survey.objects.filter(tutor_area__in=tutorArea)
        if self.min_cost and self.max_cost:
            surveys = Survey.objects.filter(
                (Q(min_cost__gte=self.min_cost) & Q(max_cost__lte=self.max_cost)) |
                (Q(min_cost__lte=self.max_cost) & Q(max_cost__gte=self.min_cost))
            )
        else:
            if self.max_cost:
                surveys = Survey.objects.filter(Q(min_cost__lte=self.max_cost) | Q(max_cost__lte=self.max_cost))
            if self.min_cost:
                surveys = Survey.objects.filter(Q(min_cost__gte=self.min_cost) | Q(max_cost__gte=self.min_cost))
        if self.subject:
            surveys = Survey.objects.filter(subjects=self.subject)
        # if self.order == "by_cost":
        #     surveys = Survey.objects.order_by('min_cost')
        #     print("GGGGGGG")
        #     print(surveys)
        context['surveys'] = surveys
        context['subjects'] = Subject.objects.all()
        context['cities'] = City.objects.all()
        return context


class BoardTutorView(ListView):
    template_name = 'board_tutor.html'
    model = TutorCabinets
    context_object_name = 'tutors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['subjects'] = Subject.objects.all()
        context['cities'] = City.objects.all()
        return context


class FilterTutorView(ListView):
    template_name = 'board_tutor.html'
    model = TutorCabinets
    context_object_name = 'tutors'

    def get(self, request, *args, **kwargs):
        self.min_cost = request.GET.get("min_cost")
        self.max_cost = request.GET.get("max_cost")
        self.subject = request.GET.get("subject")
        self.city = request.GET.get("city")
        self.format = request.GET.get("format")
        self.order = request.GET.get("order")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        tutors = TutorCabinets.objects.all()
        print("KKKKKKK")
        print(tutors)
        context = super().get_context_data(object_list=None, **kwargs)
        # if self.city and self.format == "student":
        #     tutorArea = TutorArea.objects.filter(tutor_city_id=self.city)
        #     surveys = Survey.objects.filter(student_area__in=tutorArea)
        # if self.city and self.format == "tutor":
        #     tutorArea = TutorArea.objects.filter(tutor_city_id=self.city)
        #     surveys = Survey.objects.filter(tutor_area__in=tutorArea)

        if self.subject:
            subjects = SubjectsAndCosts.objects.filter(subject_id=self.subject)
            tutors = TutorCabinets.objects.filter(subjects_and_costs__in=subjects)
        if self.min_cost and self.max_cost:
            subjects = SubjectsAndCosts.objects.filter(
                (Q(cost__gte=self.min_cost) & Q(cost__lte=self.max_cost)) |
                (Q(cost__lte=self.max_cost) & Q(cost__gte=self.min_cost)))
            tutors = TutorCabinets.objects.filter(subjects_and_costs__in=subjects)
        else:
            if self.max_cost:
                subjects = SubjectsAndCosts.objects.filter(cost__lte=self.max_cost)
                tutors = TutorCabinets.objects.filter(subjects_and_costs__in=subjects)
            if self.min_cost:
                subjects = SubjectsAndCosts.objects.filter(cost__gte=self.min_cost)
                tutors = TutorCabinets.objects.filter(subjects_and_costs__in=subjects)

        # if self.order == "by_cost":
        #     surveys = Survey.objects.order_by('min_cost')
        #     print("GGGGGGG")
        #     print(surveys)
        context['tutors'] = tutors
        context['subjects'] = Subject.objects.all()
        context['cities'] = City.objects.all()
        return context


class TutorBoardDetailPageView(DetailView):
    template_name = 'tutor_board_detail_page.html'
    model = TutorCabinets
    context_object_name = 'tutor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tutor = TutorCabinets.objects.get(id=self.object.pk)
        on_tutor_reviews = Review.objects.filter(tutor=tutor.user)
        review_rate_list = []
        for review in on_tutor_reviews:
            review_rate_list.append(review.rate)
        if len(review_rate_list) > 0:
            middle_rate = sum(review_rate_list) / len(review_rate_list)
            context['middle_rate'] = round(middle_rate, 1)

        cost_list = []
        costs = SubjectsAndCosts.objects.filter(tutors=self.object)
        exp = SubjectsAndCosts.objects.first()
        experience = exp.experience
        for cost in costs:
            cost_list.append(cost.cost)
        if len(cost_list) > 0:
            middle_cost = round(sum(cost_list) / len(cost_list))
            context['middle_cost'] = middle_cost
        educations = tutor.education.all()

        reviews = Review.objects.filter(tutor_id=tutor.user.pk)

        reviews_stats = Review.objects.filter(tutor_id=tutor.user.pk)
        if reviews_stats:
            five_sum = []
            four_sum = []
            three_sum = []
            two_sum = []
            one_sum = []
            for rate in reviews_stats:
                if rate.rate == 5:
                    five_sum.append(rate.rate)
                if rate.rate == 4:
                    four_sum.append(rate.rate)
                if rate.rate == 3:
                    three_sum.append(rate.rate)
                if rate.rate == 2:
                    two_sum.append(rate.rate)
                if rate.rate == 1:
                    one_sum.append(rate.rate)
            five_sum = len(five_sum)
            four_sum = len(four_sum)
            three_sum = len(three_sum)
            two_sum = len(two_sum)
            one_sum = len(one_sum)
            summary_rate = five_sum + four_sum + three_sum + two_sum + one_sum
            proportion_five_sum = five_sum * 100 / summary_rate
            proportion_four_sum = four_sum * 100 / summary_rate
            proportion_three_sum = three_sum * 100 / summary_rate
            proportion_two_sum = two_sum * 100 / summary_rate
            proportion_one_sum = one_sum * 100 / summary_rate

            context['proportion_five_sum'] = round(proportion_five_sum)
            context['proportion_four_sum'] = round(proportion_four_sum)
            context['proportion_three_sum'] = round(proportion_three_sum)
            context['proportion_two_sum'] = round(proportion_two_sum)
            context['proportion_one_sum'] = round(proportion_one_sum)

            context['five_sum'] = five_sum
            context['four_sum'] = four_sum
            context['three_sum'] = three_sum
            context['two_sum'] = two_sum
            context['one_sum'] = one_sum

        context['tutor'] = tutor
        context['reviews'] = on_tutor_reviews
        context['reviews_count'] = len(review_rate_list)
        context['educations'] = educations
        context['experience'] = experience
        context['reviews'] = reviews

        return context


class StudentBoardDetailPageView(DetailView):
    template_name = 'student_board_detail_page.html'
    model = Survey
    context_object_name = 'survey'
