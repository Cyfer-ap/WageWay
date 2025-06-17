from django import forms
from .models import Review

class BaseReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="⭐ Overall Rating (Required)"
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label="🗒️ Written Feedback (Optional)"
    )

    class Meta:
        model = Review
        fields = ['rating', 'feedback']

# Poster reviewing Worker
class PosterToWorkerReviewForm(BaseReviewForm):
    timeliness = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        required=False,
        widget=forms.RadioSelect,
        label="⏱ Timeliness"
    )
    quality_of_work = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        required=False,
        widget=forms.RadioSelect,
        label="🔧 Quality of Work"
    )
    communication_worker = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        required=False,
        widget=forms.RadioSelect,
        label="💬 Communication"
    )
    professionalism = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        required=False,
        widget=forms.RadioSelect,
        label="🤝 Professionalism"
    )
    recommend_worker = forms.ChoiceField(
        choices=[(True, 'Yes'), (False, 'No')],
        required=False,
        widget=forms.RadioSelect,
        label="📌 Would You Recommend This Worker?"
    )

    class Meta(BaseReviewForm.Meta):
        fields = BaseReviewForm.Meta.fields + [
            'timeliness', 'quality_of_work', 'communication_worker',
            'professionalism', 'recommend_worker'
        ]

# Worker reviewing Poster
class WorkerToPosterReviewForm(BaseReviewForm):
    clarity_of_instructions = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        required=False,
        widget=forms.RadioSelect,
        label="🎯 Clarity of Instructions"
    )
    communication_poster = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        required=False,
        widget=forms.RadioSelect,
        label="💬 Communication"
    )
    fairness_in_payment = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        required=False,
        widget=forms.RadioSelect,
        label="💸 Fairness in Payment"
    )
    respect_behavior = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        required=False,
        widget=forms.RadioSelect,
        label="🙌 Respect & Behavior"
    )
    work_again = forms.ChoiceField(
        choices=[(True, 'Yes'), (False, 'No')],
        required=False,
        widget=forms.RadioSelect,
        label="📌 Would You Work With This Client Again?"
    )

    class Meta(BaseReviewForm.Meta):
        fields = BaseReviewForm.Meta.fields + [
            'clarity_of_instructions', 'communication_poster',
            'fairness_in_payment', 'respect_behavior', 'work_again'
        ]

