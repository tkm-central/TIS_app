import json

import requests
from django import forms
from django.conf import settings

DEFAULT_AMAZON_ML_ENDPOINT="https://realtime.machinelearning.us-east-1.amazonaws.com"

EMP_LENGTH_CHOICES = (
    (0.0, "無し"),
    (0.5, "1年未満"),
    (1.0, "満1年"),
    (2.0, "満2年"),
    (3.0, "満3年"),
    (4.0, "満4年"),
    (5.0, "満5年"),
    (6.0, "満6年"),
    (7.0, "満7年"),
    (8.0, "満8年"),
    (9.0, "満9年"),
    (10.0, "10年以上"),
)

HOME_OWNERSHIP_CHOICES = (
    ("RENT", "賃貸"),
    ("OWN", "持ち家"),
    ("MORTGAGE", "持ち家(抵当)"),
    ("OTHER", "その他"),
)

GRADE_CHOICES = {
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ("F", "F"),
    ("G", "G"),
}


SUB_GRADE_CHOICES = {
    ("A1", "A1"),
    ("A2", "A2"),
    ("A3", "A3"),
    ("A4", "A4"),
    ("A5", "A5"),
    ("B1", "B1"),
    ("B2", "B2"),
    ("B3", "B3"),
    ("B4", "B4"),
    ("B5", "B5"),
    ("C1", "C1"),
    ("C2", "C2"),
    ("C3", "C3"),
    ("C4", "C4"),
    ("C5", "C5"),
    ("D1", "D1"),
    ("D2", "D2"),
    ("D3", "D3"),
    ("D4", "D4"),
    ("D5", "D5"),
    ("E1", "E1"),
    ("E2", "E2"),
    ("E3", "E3"),
    ("E4", "E4"),
    ("E5", "E5"),
    ("F1", "F1"),
    ("F2", "F2"),
    ("F3", "F3"),
    ("F4", "F4"),
    ("F5", "F5"),
    ("G1", "G1"),
    ("G2", "G2"),
    ("G3", "G3"),
    ("G4", "G4"),
    ("G5", "G5"),
}

class ExaminationForm(forms.Form):
    loan_amnt = forms.DecimalField(
        label="ご希望の融資額($)",
        min_value=0,
        max_value=100000,
        required=True,
        widget=forms.NumberInput()
    )
    emp_title = forms.CharField(
        label="職種",
        max_length=60,
        required=False,
        widget=forms.TextInput()
    )
    emp_length = forms.ChoiceField(
        label="勤続年数",
        choices=EMP_LENGTH_CHOICES,
        required=True,
        widget=forms.Select()
    )
    annual_inc = forms.DecimalField(
        label="年収($)",
        min_value=0,
        required=True,
        widget=forms.NumberInput()
    )
    home_ownership = forms.ChoiceField(
        label="自宅の所有状況",
        choices=HOME_OWNERSHIP_CHOICES,
        required=True,
        widget=forms.Select()
    )
    int_rate = forms.DecimalField(
        label="ローン金利(％)",
        min_value=0,
        max_value=100,
        max_digits=4,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput()
    )
    grade = forms.ChoiceField(
        label="グレード",
        choices=GRADE_CHOICES,
        required=True,
        widget=forms.Select()
    )
    sub_grade = forms.ChoiceField(
        label="サブグレード",
        choices=SUB_GRADE_CHOICES,
        required=False,
        widget=forms.Select()
    )
    bc_open_to_buy = forms.DecimalField(
    label="bc_open_to_buy(0-5437-454843)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )
    all_util = forms.DecimalField(
    label="all_util(0-62-161)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )
    percent_bc_gt_75 = forms.DecimalField(
    label="percent_bc_gt_75(0-33.3-100)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )
    bc_util = forms.DecimalField(
    label="bc_util(0-57.4-189.8)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )
    mort_acc = forms.DecimalField(
    label="mort_acc(0-1-37)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )
    total_bc_limit = forms.DecimalField(
    label="total_bc_limit(0-15400-474600)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )
    percent_bc_gt_75 = forms.DecimalField(
    label="percent_bc_gt_75(0-33.3-100)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )
    total_rev_hi_lim = forms.DecimalField(
    label="total_rev_hi_lim(0-25200-1070650)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )
    dti = forms.DecimalField(
    label="dit(0-18.21-39.99)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )
    tot_hi_cred_lim = forms.DecimalField(
    label="tot_hi_cred_lim(2500-123513-9999999)",
    min_value=0,
    required=False,
    widget=forms.NumberInput()
    )


    def predict_loan_status(self):
        model_id = getattr(settings, "AMAZON_ML_MODEL_ID")
        amazon_ml_endpoint = getattr(settings, "AMAZON_ML_ENDPOINT", DEFAULT_AMAZON_ML_ENDPOINT)
        api_gateway_endpoint = getattr(settings, "API_GATEWAY_ENDPOINT")
        payload = {
            "MLModelId": model_id,
            "PredictEndpoint": amazon_ml_endpoint,
            "Record": {
                "loan_amnt": str(self.cleaned_data['loan_amnt']),
                "emp_title": self.cleaned_data['emp_title'],
                "emp_length": self.cleaned_data['emp_length'],
                "annual_inc": str(self.cleaned_data['annual_inc']),
                "home_ownership": self.cleaned_data['home_ownership'],
                "int_rate": str(self.cleaned_data['int_rate']),
                "grade": self.cleaned_data['grade'],
                "sub_grade":self.cleaned_data['sub_grade'],
                "bc_open_to_buy": str(self.cleaned_data['bc_open_to_buy']),
                "all_util": str(self.cleaned_data['all_util']),
                "percent_bc_gt_75": str(self.cleaned_data['percent_bc_gt_75']),
                "bc_util": str(self.cleaned_data['bc_util']),
                "mort_acc": str(self.cleaned_data['mort_acc']),
                "total_bc_limit": str(self.cleaned_data['total_bc_limit']),
                "total_rev_hi_lim": str(self.cleaned_data['total_rev_hi_lim']),
                "dti": str(self.cleaned_data['dti']),
                "tot_hi_cred_lim": str(self.cleaned_data['tot_hi_cred_lim']),
            }
        }
        response = requests.post(api_gateway_endpoint, data=json.dumps(payload))
        return response.json()
