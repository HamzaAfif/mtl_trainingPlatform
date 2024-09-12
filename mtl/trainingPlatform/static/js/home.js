
let selectedOption = ''; 
let selectedSubOption = ''; 
let selectedComfortLevel = ''; 
let selectedAnswers = {}; 
let questionTexts = {}; 
let answerTexts = {}; 
let fetchedQuestions = [];

function selectOption(choice) {
  document.getElementById('red-teaming-btn').classList.remove('btn-selected');
  document.getElementById('blue-teaming-btn').classList.remove('btn-selected');
  
  if (choice === 'red') {
    document.getElementById('red-teaming-btn').classList.add('btn-selected');
    selectedOption = 'red_team';
  } else if (choice === 'blue') {
    document.getElementById('blue-teaming-btn').classList.add('btn-selected');
    selectedOption = 'blue_team';
  }
  
  questionTexts['question1'] = 'What are you more into?';
  answerTexts['question1'] = choice === 'red_team' ? 'Red Teaming' : 'Blue Teaming';
  
  updateQuestions();
}

function updateQuestions() {
            let nextQuestionText = '';
            let optionsHtml = '';

            
            selectedSubOption = '';
            selectedAnswers = {}; 
            document.getElementById('questions-container').innerHTML = ''; 

            if (selectedOption === 'red_team') {
              nextQuestionText = "You chose Red Teaming. What do you prefer in Red Teaming?";
              optionsHtml = `
                <button class="btn btn-outline-secondary btn-lg" onclick="selectSubOption('Pen_Testing')">Pen Testing</button>
                <button class="btn btn-outline-secondary btn-lg" onclick="selectSubOption('Vulnerability_Assessment')">Vulnerability Assessment</button>
              `;
            } else if (selectedOption === 'blue_team') {
              nextQuestionText = "You chose Blue Teaming. What do you prefer in Blue Teaming?";
              optionsHtml = `
                <button class="btn btn-outline-secondary btn-lg" onclick="selectSubOption('SOC')">SOC Analyst</button>
                <button class="btn btn-outline-secondary btn-lg" onclick="selectSubOption('Digital_forensics')">Digital Forensics</button>
                <button class="btn btn-outline-secondary btn-lg" onclick="selectSubOption('Threat_hunting')">Threat Hunting</button>
              `;
            }

            document.getElementById('next-question').innerHTML = nextQuestionText;
            document.getElementById('options-container').innerHTML = optionsHtml;

            document.getElementById('question2').style.display = 'block';
            
}

function selectSubOption(option) {
  const buttons = document.querySelectorAll('#options-container .btn');
  buttons.forEach(button => button.classList.remove('btn-selected'));

  const selectedButton = document.querySelector(`#options-container .btn[onclick="selectSubOption('${option}')"]`);
  if (selectedButton) {
    selectedButton.classList.add('btn-selected');
    selectedSubOption = option;
  }
  
  questionTexts['question2'] = 'You chose ' + (selectedOption === 'red_team' ? 'Red Teaming' : 'Blue Teaming') + '. What do you prefer in ' + (selectedOption === 'red' ? 'Red Teaming' : 'Blue Teaming') + '?';
  answerTexts['question2'] = option;
  
  
  console.log("got here "); 
  loadQuestions();
}




async function loadQuestions() {
  try {
    const response = await fetch(window.questionsUrl);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();

    console.log('Fetched data:', data);

    let questions = [];
    if (selectedOption === 'blue_team') {
      if (selectedSubOption === 'SOC') {
        questions = data.blue_team.SOC;
      } else if (selectedSubOption === 'Threat_hunting') {
        questions = data.blue_team.Threat_hunting;
      } else if (selectedSubOption === 'Digital_forensics') {
        questions = data.blue_team.Digital_forensics;
      }
    } else if (selectedOption === 'red_team') {
      if (selectedSubOption === 'Pen_Testing') {
        questions = data.red_team.Pen_Testing;
      } else if (selectedSubOption === 'Vulnerability_Assessment') {
        questions = data.red_team.Vulnerability_Assessment;
      }
    }

    console.log('Questions loaded:', questions); 

    if (!questions || questions.length === 0) {
      throw new Error('No questions found for the selected options');
    }

    // Store fetched questions for later use
    fetchedQuestions = questions;

    const questionsHtml = questions.map((q, index) => `
      <div class="question mt-4" data-question-index="${index}">
        <h5 class="text-dark">${q.question}</h5>
        <div class="d-flex flex-wrap justify-content-center gap-3 mt-3">
          ${q.options.map((opt, optIndex) => `
            <button class="btn btn-outline-secondary btn-lg" onclick="selectAnswer(${index}, ${optIndex})">${opt}</button>
          `).join('')}
        </div>
      </div>
    `).join('');

    document.getElementById('questions-container').innerHTML = questionsHtml;
    document.getElementById('questions-container').style.display = 'block';
    document.getElementById('save-button').style.display = 'none';
  } catch (error) {
    console.error('Error loading questions:', error);
    alert('Failed to load questions. Please try again.');
  }
}

function selectAnswer(questionIndex, answerIndex) {
  // Save the selected answer for the question
  selectedAnswers[questionIndex] = {
    answerIndex: answerIndex,
    answerText: fetchedQuestions[questionIndex].options[answerIndex]
  };

  // Update UI to reflect the selected answer
  const buttons = document.querySelectorAll(`#questions-container .question[data-question-index="${questionIndex}"] .btn`);
  buttons.forEach((button, index) => {
    button.classList.toggle('btn-selected', index === answerIndex);
  });

  // Check if all questions have been answered
  const allAnswered = Object.keys(selectedAnswers).length === fetchedQuestions.length;
  document.getElementById('save-button').style.display = allAnswered ? 'block' : 'none';
}


function saveAnswers(username) {
    const dataToSend = {
      selectedOption,
      selectedSubOption,
      selectedComfortLevel,
      username,
      answers: Object.keys(selectedAnswers).map(key => ({
        question: fetchedQuestions[key].question, 
        answer: selectedAnswers[key].answerText 
      })),
    };
  
    console.log('Sending data:', dataToSend); // Log the data being sent
  
    fetch('/save-answers/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(dataToSend)
    })
    .then(response => {
      console.log('Response received:', response); // Log the response object
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Failed to save answers');
      }
    })
    .then(data => {
      console.log('Success:', data);
      window.location.reload(); // Refresh the page
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('Error saving answers.');
    });
}
  
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}
  
  