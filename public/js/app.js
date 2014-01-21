var todoApp = angular.module('todoApp', ['firebase']);

todoApp.controller("LoginController", ["$scope", "$firebase", "$firebaseSimpleLogin", function($scope, $firebase, $firebaseSimpleLogin) {
  var ref = new Firebase("https://is429-demo.firebaseio.com/");
  $scope.auth = $firebaseSimpleLogin(ref);
}]).controller('TodoController', function($scope, $firebase) {

  $scope.loaded = false;

  var ref = new Firebase('https://is429-demo.firebaseio.com/todos');
  $scope.todos = $firebase(ref);
  $scope.todos.$bind($scope, "todos");
  
  $scope.addTodo = function(title) {
    if (title !== '') {
      // Reset the title to an empty string
      $scope.newTodoTitle = '';
      // Each todo is an object with a title, completed status and a generated ID
      // Set the newly created todo as a child in the todo collection
      var id = generateID();
      $scope.todos.$child(id).$set({
        title: title,
         completed: false,
         id: id
      });
    } else {
      alert("Please type something!");
    }
  };

  $scope.changeCompleted = function(todo) {
    // Update the todo
    $scope.todos.$child(todo.id).$set(todo);
    var message = (todo.completed === true) ? 'Task Completed!' : 'Task Uncompleted!';
  };

  $scope.removeCompletedItems = function() {
    // If a todo is completed, delete it
    $scope.todos.$getIndex().forEach(function(index) {
      if ($scope.todos[index].completed === true) {
        $scope.todos.$remove(index);
      }
    });
  };

  // Random ID generator
  function generateID() {
    var chars, x, length = 10;
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-=";
    var name = [];
    for (x = 0; x < length; x++) {
      name.push(chars[Math.floor(Math.random() * chars.length)]);
    }
    var id = name.join('');
    if ($scope.todos.$getIndex().indexOf(id) === -1) {
      return id;
    } else {
      generateId();
    }
  }


});