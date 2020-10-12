// Import modules.
const http = require('http');
const fs = require('fs');
const injectModule = require('./flip-the-script');

// Set web server constants.
const HOST = '0.0.0.0';
const PORT = 3000;

// Terminate on Ctrl+C
process.on('SIGINT', function() {
    process.exit();
});

// Read files from disk.
const getFile = function(filename) {
  try {
    return fs.readFileSync(filename);
  } catch (e) {
    return `File not found: ${filename}.`
  }
};

// Read source files.
const index = getFile('index.html');
const client = getFile('client.js');
const flip = getFile('flip-the-script.js');
const flag = getFile('flag.txt');

// Check the flag
const getFlag = function(showMessage) {
  return function() {
    showMessage(flag);
  }
};

// Output data.
const showMessage = function(output) {
  return function(message) {
    output.push(message);
  }
};

const processAnswer = function(req, output) {
  inputText = req.headers[injectModule.HEADER];
  printer = showMessage(output);
  if (inputText !== undefined) {
    injectModule.checkInput(inputText, printer, getFlag(printer), true);
  } else {
    printer(`Please provide an answer in the "${injectModule.HEADER}" header.`);
  }
};

// Set up a web server.

const send = function(res, message, contentType) {
  res.statusCode = 200;
  res.setHeader('Content-Type', contentType);
  res.end(message);
};

const server = http.createServer((req, res) => {
  const output = [];
  var inputText, i, html = '';

  switch (req.url) {
    case '/':
    case '/index.html':
      send(res, index, 'text/html');
      break;
    case '/flip-the-script.js':
      send(res, flip, 'text/javascript');
      break;
    case '/client.js':
      send(res, client, 'text/javascript');
      break;
    case '/submit':
      processAnswer(req, output);
      for (i = 0; i < output.length; i++) {
        html += `<div>${output[i]}</div>`;
      } 
      send(res, html, 'text/plain');
      break;
    default:
      send(res, 'Invalid file: ' + req.url, 'text/plain');
  }
});

server.listen(PORT, HOST, () => {
  console.log(`Server running at http://${HOST}:${PORT}/`);
});

