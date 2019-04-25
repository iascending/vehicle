var gulp = require('gulp');
var watch = require('gulp-watch');
var browserSync = require('browser-sync').create();

gulp.task('watch', function(){
    notify: false;
    //start Django server
    gulp.start('startDjango');

    browserSync.init({
      // notify: false,
      // localOnly: true,
      // server: {
      //   baseDir: "src"
      // }
      proxy: {
        target: 'http://127.0.0.1:8000/',
      },
      port: process.env.PORT || 8000,
    });

    watch('./src/**/*.html', function(){
        browserSync.reload();
    });

    watch('./src/static/styles/**/*.css', function(){
        gulp.start('cssInject');
    });

    watch('./src/static/scripts/**/*.js', function(){
      gulp.start('scriptsRefresh');
    });
});

gulp.task('cssInject', ['styles'], function(){
  return gulp.src('./src/static/temp/styles.css')
      .pipe(browserSync.stream());
});

gulp.task('scriptsRefresh', ['scripts'], function(){
  browserSync.reload();
});
