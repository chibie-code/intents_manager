# intents_manager
A simple Kivy app/tool I created to easily edit and create intents files for a simple rule-based python chatbot app

​It's a JSON file editor of sorts, to simply import, add new, edit selected existing, delete
![](https://github.com/chibie-code/intents_manager/blob/main/gif/add_edit.gif)

This wasn't made dynamic for any kind of JSON file structure. I might be able to do something like that but this app was made while learning Kivy as a beginner and I didn't have much time to add complex features.
The required/recognized file type is JSON and file structure must be something like this:
```JSON
{
    "intents": [
        {
            "tag": "tag_name",
            "patterns": [
                "Nice to meet you",
                "Lovely to meet you",
                "Pleased to meet you",
                "Good to see you",
                "It's great to see you"
            ],
            "responses": [
                "Delightful to meet you to",
                "Always appreciate your presence, friend",
                "Even better to see you",
                "Great to see you to"
            ],
            "context": []
        }
    ]
}
```
Executable file in 'cd sample_executable'