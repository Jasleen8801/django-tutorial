from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


class LandingPageView(TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request, "landing.html")


class LeadListView(ListView):
    template_name = "lead_list.html"
    queryset = Lead.objects.all()
    # leads to be replaced by object_list in the template
    context_object_name = "leads"


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads,
    }
    return render(request, "lead_list.html", context=context)


class LeadDetailView(DetailView):
    template_name = "lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead,
    }
    return render(request, "lead_detail.html", context=context)


class LeadCreateView(CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return resolve_url("leads:lead-list")


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": LeadModelForm(),
    }
    return render(request, "lead_create.html", context=context)


# def lead_create(request):
#     # print(request.POST)
#     form = LeadForm()
#     if request.method == "POST":
#         # print("Receiving a POST request")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             # print("The form is valid")
#             # print(form.cleaned_data)
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             age = form.cleaned_data["age"]
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent,
#             )
#             # print("Lead has been created")
#             return redirect("/leads")
#     context = {
#         "form": LeadForm(),
#     }
#     return render(request, "lead_create.html", context=context)


class LeadUpdateView(UpdateView):
    template_name = "lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return resolve_url("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead,
    }
    return render(request, "lead_update.html", context=context)


# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             age = form.cleaned_data["age"]
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect("/leads")
#     context = {
#         "form": form,
#         "lead": lead,
#     }
#     return render(request, "lead_update.html", context=context)


class LeadDeleteView(DeleteView):
    template_name = "lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return resolve_url("leads:lead-list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")
