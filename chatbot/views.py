import requests
import json
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import ChatPrompt, Product
from .forms import ChatForm  # You'll need to create this form

def home(request):
    """Home page view"""
    return render(request, 'chatbot/home.html')

def chatbot(request):
    """Enhanced Chatbot view with all features"""
    products = Product.objects.filter(in_stock=True)
    prompt_obj = ChatPrompt.objects.first()
    
    # Handle form submission
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            
            # Get system prompt (from DB or file)
            system_prompt = get_system_prompt(prompt_obj)
            
            try:
                # Enhanced API call with timeout
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": settings.SITE_URL,
                        "X-Title": settings.SITE_NAME,
                    },
                    json={  # Using json parameter instead of data=json.dumps()
                        "model": "deepseek/deepseek-r1-0528:free",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500  # Limit response length
                    },
                    timeout=15  # Add timeout
                )
                
                response.raise_for_status()
                api_response = response.json()
                bot_response = api_response['choices'][0]['message']['content']
                
                # Store conversation in session
                if 'conversation' not in request.session:
                    request.session['conversation'] = []
                request.session['conversation'].append({
                    'user': user_input,
                    'bot': bot_response
                })
                
            except requests.exceptions.RequestException as e:
                bot_response = f"Sorry, our chat service is currently unavailable. Error: {str(e)}"
                messages.error(request, "Failed to get response from chatbot")
            except KeyError as e:
                bot_response = "Sorry, there was an error processing the response."
                messages.error(request, "Invalid response format from API")
            
            return render(request, 'chatbot/chatbot.html', {
                'form': form,
                'bot_response': bot_response,
                'user_input': user_input,
                'products': products,
                'conversation': request.session.get('conversation', [])
            })
    else:
        form = ChatForm()
    
    return render(request, 'chatbot/chatbot.html', {
        'form': form,
        'products': products,
        'conversation': request.session.get('conversation', [])
    })

def get_system_prompt(prompt_obj=None):
    """Get prompt from DB, file, or use default"""
    if prompt_obj:
        return prompt_obj.prompt_text
    
    # Try to get prompt from file
    try:
        prompt_file = os.path.join(settings.BASE_DIR, 'chatbot', 'prompts', 'system_prompt.txt')
        with open(prompt_file, 'r') as f:
            prompt_text = f.read().strip()
            # Save to DB for future use
            ChatPrompt.objects.create(prompt_text=prompt_text)
            return prompt_text
    except (FileNotFoundError, IOError):
        pass
    
    # Default fallback
    default_prompt = """You are a helpful assistant for PATIL BATTERIES AND POWER SOLUTIONS. 
    Help customers find the right battery based on their requirements. 
    Be friendly and professional. Only provide information about products we actually have in stock."""
    ChatPrompt.objects.create(prompt_text=default_prompt)
    return default_prompt