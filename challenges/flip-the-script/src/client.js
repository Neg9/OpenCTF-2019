// DOM elements
const inputField = document.getElementById('input');
const output = document.getElementById('output');

const showMessage = function(html) {
  let div = document.createElement('div');
  div.innerHTML = html;
  output.appendChild(div);
};

const getFlag = function(showMessage) {
  const request = new XMLHttpRequest();
  if (!request) {
    showMessage(
      'Error while creating XMLHTTP instance.' +
      ' Use a different browser?'
    )
  }
  request.onreadystatechange = sendRequest;
  request.open('GET', '/submit');
  request.setRequestHeader(HEADER, inputField.value || '');
  request.send();

  function sendRequest() {
    output.innerHTML = '';
    if (request.readyState === XMLHttpRequest.DONE) {
      if (request.status === 200) {
        showMessage(request.responseText);
      } else {
        showMessage('There was an error while sending the request.');
      }
    }
  }
};

const ignoreKeys = {
  '16': 'shift',
  '17': 'control',
  '37': 'left',
  '38': 'up',
  '39': 'right',
  '40': 'down'
};

inputField.onkeyup = function(e) {
  if (!(e.keyCode in ignoreKeys)) {
    output.innerHTML = '';
    let text = this.value;
    injection.checkInput(text, showMessage, getFlag);
  }
};

// Initialization code
document.getElementById('input').dispatchEvent(new Event('keyup'));

