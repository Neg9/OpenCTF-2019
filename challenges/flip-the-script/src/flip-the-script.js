// Constants
const HEADER = 'answer';

const ScriptInjection = (function(exports) {
  // The maximum number of total characters.
  const maxInputLength = 28;

  // The maximum number of * characters.
  const maxStarCount = 3;

  // A whitelist of characters.
  const validCharacters = (function() {
    const allowed = `'"/*+target.exploit`,
          lookup = {};
    var character;

    for (var i = 0; i < allowed.length; i++) {
      character = allowed.charAt(i);
      lookup[character] = true;
    }
    return lookup;
  })();

  const cases = [
    {name: 'unquoted', prefix: '', suffix: ''},
    {name: 'double-quoted', prefix: '"', suffix: '"'},
    {name: 'single-quoted', prefix: "'", suffix: "'"},
  ];

  const messages = {
    true: '<span class="pass">succeeded</span>',
    false: '<span class="fail">failed</span>'
  };

  const newTarget = function() {
    let accessed = false;
    return {
      get exploit() {
        accessed = true;
      },
      wasAccessed: function() {
        return accessed;
      }
    };
  };

  const checkCase = function(text, i) {
    const target = newTarget(),
          testCase = cases[i];

    try {
      eval(testCase.prefix + text + testCase.suffix);
      return target.wasAccessed();
    } catch(error) {
      return false;
    }
  }

  const validateInput = function(text) {
    var character;
    const invalid = [],
          length = text.length,
          starCount = text.split('*').length - 1;

    if (length > maxInputLength) {
      return (
        `Input is too long: have ${length} characters,` +
        ` but the max is ${maxInputLength}.`
      );
    }

    for (var i = 0; i < text.length; i++) {
      character = text.charAt(i)
      if (!(character in validCharacters)) {
        invalid.push('"' + character + '"');
      }
    }

    if (invalid.length > 0) {
      invalid.sort();
      return `Invalid characters: ${invalid.join(', ')}`;
    }

    if (starCount > maxStarCount) {
      return (
        `You used ${starCount} * characters,` +
        ` but you can use at most ${maxStarCount}.`
      );
    }

    // No errors
    return null;
  };

  const processInput = function(text, showMessage, getFlag, server) {
    var result, total = 0;

    for (var i = 0; i < cases.length; i++) {
      result = checkCase(text, i);
      showMessage(`Case "${cases[i].name}" ${messages[result]}.`);
      total += result;
    }
    
    if (total === cases.length) {
      getFlag(showMessage);
    } else if (server !== undefined) {
      showMessage('Please get it working on the client side :-)');
    }
  };

  const checkInput = function(text, showMessage, getFlag, server) {
    const errorText = validateInput(text);
    if (errorText) {
      showMessage(errorText);
    } else {
      processInput(text, showMessage, getFlag, server);
    }
  };

  // Make this code accessible.
  exports.checkInput = checkInput;
  exports.HEADER = HEADER;
}(typeof exports === 'undefined' ? this.injection = {} : exports));

