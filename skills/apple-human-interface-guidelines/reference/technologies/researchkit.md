# ResearchKit Design Guidelines

Guidelines for designing research apps that let people participate in medical studies using the ResearchKit framework. Supported on iOS/iPadOS only.

## Onboarding Experience

Onboarding screens must follow this exact order:

**Introduction → Eligibility → Informed Consent → Permission to Access Data**

These screens aren't typically revisited once completed, so clarity is essential.

### 1. Introduction
- Clearly describe the subject and purpose of your study
- Provide a call to action to join
- Allow existing participants to quickly log in and continue an in-progress study

### 2. Determine Eligibility
- Determine eligibility as soon as possible — before the consent section
- Only present eligibility requirements necessary for your study
- Use simple, straightforward language
- Make it easy to enter information

### 3. Get Informed Consent
- Make sure participants understand the study before getting consent
- Break long consent forms into easily digestible sections (data gathering, data use, benefits, risks, time commitment, withdrawal, etc.)
- Use simple language for high-level overviews; provide detailed explanations via a "Learn More" button
- Participants must be able to view the entire consent form before agreeing
- Optionally provide a quiz testing participant understanding
- After agreement: show confirmation dialog → collect signature → collect contact details
- Email participants a PDF of the consent form
- Ensure compliance with applicable App Store Guidelines

### 4. Request Permission to Access Data
- Clearly explain why the app needs access to location, Health, or other data
- Don't request access to data that isn't critical to the study
- Request notification permissions if needed

## Conducting Research

Studies use surveys, active tasks, or both.

### Survey Design
- Tell participants how many questions there are and estimated duration
- Use one screen per question
- Show progress through the survey
- Keep surveys as short as possible — several short surveys work better than one long survey
- Use standard font for questions, slightly smaller font for explanatory text
- Tell participants when the survey is complete

### Active Tasks
Active tasks require participant engagement (speaking, tapping, walking, memory tests).

- Describe how to perform the task using clear, simple language
- Explain requirements (timing, specific circumstances)
- Make sure participants can tell when the task is complete

## Profile & Dashboard

Both screens should be accessible at all times in the app.

### Profile Screen
- Let participants edit data that may change during the study (weight, sleep habits, etc.)
- Remind them of upcoming activities
- Provide a way to leave the study
- Show consent document and privacy policy

### Dashboard
- Show daily progress, weekly assessments, and activity results
- Optionally compare participant results with aggregated results from others
- Use to motivate continued participation