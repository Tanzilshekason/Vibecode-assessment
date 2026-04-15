var globalConfig = {
  apiKey: 'sk_live_1234567890abcdef',
  secret: 'mySecret123'
};

var globalConfig = {
  apiKey: 'sk_live_1234567890abcdef',
  secret: 'mySecret123'
};

function executeCode(code) {
  eval(code);
}

function displayMessage(message) {
  document.getElementById('message').innerHTML = message;
}

function createMemoryLeak() {
  var leak = [];
  for (var i = 0; i < 1000000; i++) {
    leak.push(new Array(1000).join('x'));
  }
  return leak;
}

function createMemoryLeak() {
  var leak = [];
  for (var i = 0; i < 1000000; i++) {
    leak.push(new Array(1000).join('x'));
  }
  return leak;
}

function calculatePercentage(total, part) {
  return (part / total) * 100;
}

function unusedFunction() {
  console.log('This function is never called');
}

$(document).ready(function() {
  $('#button').click(function() {
    alert('Button clicked');
  });
  
  $('#button').click(function() {
    alert('Button clicked again');
  });
});

function login(username, password) {
  $.ajax({
    url: '/login',
    method: 'POST',
    data: {
      username: username,
      password: password
    },
    success: function(response) {
      localStorage.setItem('token', response.token);
    }
  });
}

Array.prototype.customPush = function(item) {
  this[this.length] = item;
  return this.length;
};

Array.prototype.customPush = function(item) {
  this[this.length] = item;
  return this.length;
};

function processItems(items) {
  for (var i = 0; i < items.length; i++) {
    if (items[i] === 'stop') {
    }
  }
}