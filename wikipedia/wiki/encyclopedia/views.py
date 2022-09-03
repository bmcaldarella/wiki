from contextlib import _RedirectStream
from http.client import HTTPResponse
from django.shortcuts import render, redirect
import markdown2
from . import util
from django import forms 
from django.http import HttpResponseRedirect, request
import random
from django.urls import reverse

class Form(forms.Form): 
    title = forms.CharField(label="Title" )
    content = forms.CharField(widget=forms.Textarea, label="Content")

    class Edit(forms.Form):
        textarea = forms.CharField(widget=forms.Textarea(), label='')


def index(request):
     return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def topic(request, title):
    markdown = util.get_entry(title)
    if  markdown:
        html = markdown2.markdown( markdown)
        return render(request, "encyclopedia/print.html", {
            "title": title,
            "content": html
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": f" Wiki page : '{title}' not found"
        })




def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    for title in entries:
        if (query.upper() == title or query.lower() == title or query.capitalize() == title):
            return topic(request,title)
            break
        elif query in title:
            return render(request, "encyclopedia/results.html", { "entries": entries, "query": query})
            break
    return render(request, "encyclopedia/error.html", {
        "message": f"Wiki page titled {query} not found"

    })



def new(request):
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) == None :
                util.save_entry(title=title,content=content)
                return redirect(topic,title)
            else :
                return render(request, "encyclopedia/new.html", {
                    "error": 1
                })
    return render(request, "encyclopedia/new.html", {
        "error": 0,
        
        "form": Form()
        
        
    })
    
def randomq(request):
    entries=util.list_entries()
    entry = random.choice(entries)
    return redirect(topic,entry)

def edit(request, entry):
    content = util.get_entry(entry)
    if request.method=="POST":
        content = request.POST.get("content")
        util.save_entry(title=entry, content=content)
        return redirect(topic, entry)

    if content:
        return render(request, "encyclopedia/edit.html",{
        "title": entry,
        "content" : util.get_entry(entry)
    })

    else:
        return HttpResponseRedirect(reverse('index'))