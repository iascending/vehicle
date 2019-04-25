// start Python Django server
var gulp = require('gulp');
var path = require('path');
var spawn = require('child_process').spawn;

gulp.task('startDjango', function(cb){
  var proDir = path.resolve(__dirname, '../../src');
  var envDir = path.resolve(__dirname, '../../bin');
  console.log(proDir);

  var cmd    = spawn('python3', [proDir+'/manage.py', 'runserver'],
                  {cwd: envDir, stdio: 'inherit'}
                  // {cwd: envDir, stdio: 'inherit'}
               );
  cmd.on('close', function(code){
    console.log('startDjango exited with code ' + code);
    cb(code);
  });
});
