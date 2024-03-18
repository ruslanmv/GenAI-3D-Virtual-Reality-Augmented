# Creating a Smart NPC with Watsonx.ai LLM in Unreal Engine 5

In this tutorial, we will learn how to create a smart NPC (Non-Player Character) from scratch using Watsonx.ai LLM to answer and respond to questions. Let's break down the steps in more detail:

## Introduction

In this we brief introduction to the concept of creating a smart NPC using Watsonx.ai LLM. The NPC, named Watson.

## Getting Started

To begin, the tutorial instructs you to visit the website confai.com and sign up for an account. This website is where you will design and configure your AI character.

## Designing the AI Character

Once you have created an account and logged in, you are directed to the dashboard. From here, you can create a new character by clicking on the "Create New Character" button. In this step, you are prompted to give your character a name. For example, the tutorial suggests the name "Watson".

Next, you need to decide how you want your character to sound. The tutorial suggests choosing a young U.S masculine voice for your character.

After deciding the voice, you will write the backstory for your character. The backstory provides information that the AI will use to respond to questions. You can either manually write the backstory or use another AI tool like Watsonx.ai LLM to generate it. For example, the tutorial presents a generated backstory where the character used to be a Sales Assistant. You can use this generated backstory or write your own.

Once you have entered the character's name, chosen the voice, and written the backstory, you can click on the "Create Character" button to proceed.

## Unreal Engine Integration

In this section, the tutorial guides you on integrating the conf AI plugin into Unreal Engine.

1. Go to the Unreal Engine Marketplace and search for "conf AI". Once you find the plugin, download and install it. Make sure to choose the version that matches your Unreal Engine installation.

2. After installing the plugin, open your Unreal Engine project. In the editor, go to Edit > Plugins. Search for "conf AI" and check the box to enable the plugin. The editor will prompt you to restart in order to apply the changes.

3. Once the editor restarts, you need to enable voice chat with the AI. Right-click on the content drawer and select "Show and Explore". Navigate to your project's config folder and open the default engine any file. At the top of the file, paste two lines of code that allow voice chat with the AI. The tutorial provides a link where you can copy these lines. Save the file and restart your project.

## Setting up the AI

In this section, the tutorial explains how to set up the AI character within your Unreal Engine project.

1. Open your player character in your game project. In the class settings, change the parent class to "conf AI base player".

2. To add a Meta Human to your project, go to "Quickly Add Things to the Project" and select "Meta Humans". Choose a Meta Human that you want to use for your AI character. During the Meta Human addition process, make sure to enable any missing plugins as instructed in the tutorial. After enabling the necessary plugins, you will need to restart the editor.

3. Open the Meta Human character that you added to your project. You may encounter warning messages indicating deprecated nodes. The tutorial instructs you to resolve these warnings by replacing the deprecated nodes with the suggested replacements. This step ensures that the character functions correctly.

4. In the class settings of the Meta Human character, change the parent class to "conf AI base character". This step connects the character to the conf AI system. For the animation class, set the face animation to "conf AI meta human face" and the body animation to "conf AI meta human body".

5. Save and compile the changes you made to the Meta Human character.

## API Key and Character ID

To establish the connection between the Unreal Engine project and the conf AI online platform, you need to provide an API key and character ID.

1. In Unreal Engine, navigate to Edit > Project Settings. Scroll down to find the conf AI plugin. Enter your API key, which you can obtain from the conf AI website. This key allows the Unreal Engine project to connect to your online account.

2. In the content drawer of Unreal Engine, locate the manual and open it. Inside the manual, you will find a field for entering the character ID. Copy the character ID from the conf AI online platform and paste it into the manual.

After completing the API key and character ID setup, you can hold the T button and talk to the AI character in your Unreal Engine project. You can ask questions such as "What's your name?" or "Can you tell me more about yourself?" The AI will respond accordingly.

That's it! You have successfully created a smart AI NPC using Watsonx.ai LLM and integrated it into Unreal Engine. While the tutorial demonstrates the free version of the product, there are paid versions available with additional features. I hope this detailed explanation helps you understand the steps involved. If you have any questions, feel free to ask!