
from .models import Topic
from .forms import TopicForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EntryForm
from .models import Entry


def index(request):
    return render(request, 'learning_logs/index.html')


def topics(request):
    topics = Topic.objects.order_by('date_added')
    return render(request, 'learning_logs/topics.html', {'topics': topics})


def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    entries = topic.entry_set.order_by('-date_added')

    context = {
        'topic': topic,
        'entries': entries
    }
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    return render(request, 'learning_logs/new_topic.html', {'form': form})

def new_entry(request, topic_id):
    """Add a new entry for a given topic."""
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method != 'POST':
        # No POST data, create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process it.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # don't save to database yet
            new_entry.topic = topic             # set the topic FK
            new_entry.save()                    # now save to database
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Populate form with the current entry (instance).
        form = EntryForm(instance=entry)
    else:
        # Bind form to POST data and the instance.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()  # save updates to the entry
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

