jQuery( document ).ready(function( $ ) {
$("#progressTimer").progressTimer({
                                  timeLimit: 120,
                                  warningThreshold: 10,
                                  baseStyle: 'progress-bar-warning',
                                  warningStyle: 'progress-bar-danger',
                                  completeStyle: 'progress-bar-info',
                                  onFinish: function() {
                                  console.log("I'm done");
                                  }
                                  });
});
