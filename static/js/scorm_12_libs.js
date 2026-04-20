'use strict'

// const scorm = pipwerks.SCORM;
//
// let lmsConnected;

window.scorm = pipwerks.SCORM;
window.scorm.version = '1.2';
window.lmsConnected = null;

let scormLocation = null;
let scormBlocks = null;

function handleError(msg) {
    alert(msg);
    //window.close();
}

function getProgress() {
    let location = scorm.get("cmi.location");
    let blocks = scorm.get("cmi.suspend_data");
    if ((location !== null && location !== undefined && location !== '') && (blocks !== null && blocks !== undefined && typeof blocks === 'string' && blocks !== '')) {
        scormLocation = location === '' ? null : location;
        scormBlocks = blocks === '' ? null : JSON.parse(blocks);
        window.hasScormProgress = true;
    }
}

function disableWaitingData() {
    let overlay = document.querySelector('.scorm-loader-overlay');
    let body = document.querySelector('.body-js');

    overlay.style.display = 'none';
    body.classList.remove('body-no-scroll');
}

function uploadProgress() {
    if (lmsConnected) {
        scorm.set("cmi.progress_measure", (window.progress / window.blocksCount).toString()); // progress
        scorm.set("cmi.location", window.currentLesson.toString()); // lesson
        scorm.set("cmi.suspend_data", JSON.stringify(window.blocksCountLessons)); // full progress by lessons
        scorm.save();
    }
}

function initCourse() {
    window.lmsConnected = scorm.init();
    if (lmsConnected) {
        getProgress();
        const completionStatus = scorm.get("cmi.core.lesson_status");
        window.total_time = scorm.get("cmi.total_time");
        //const successStatus = scorm.get("cmi.success_status");
        if (completionStatus === "completed") {
            handleError("Вы уже прошли этот курс.");
        }
    } else {
        console.log("Ошибка: Курс не может связаться с LMS");
    }
}

window.onload = function () {
    disableWaitingData();
    initCourse();
}
window.onbeforeunload = function () {
    if (lmsConnected) {
        scorm.quit()
    }
};

function setComplete() {
    console.log(finalScore.toString());
    if (lmsConnected) {
        scorm.set("cmi.core.score.min", "0");
        scorm.set("cmi.core.score.max", maxScore.toString());
        // scorm.set("cmi.core.score.max", "100");
        scorm.set("cmi.core.score.raw", finalScore.toString());
        // scorm.set("cmi.core.score.raw", (finalScore / maxScore * 100).toString());
        let completion = scorm.set("cmi.completion_status", "completed");
        // scorm.set("cmi.progress_measure", 1); // progress
        // scorm.set("cmi.location", ''); // lesson
        // scorm.set("cmi.suspend_data", ''); // full progress by lessons
        scorm.set("cmi.progress_measure", (window.progress / window.blocksCount).toString()); // progress
        scorm.set("cmi.location", window.currentLesson.toString()); // lesson
        scorm.set("cmi.suspend_data", JSON.stringify(window.blocksCountLessons)); // full progress by lessons
        scorm.set("cmi.session_time", window.sessionTime());
        // scorm.set("cmi.total_time", window.total_time);
        //let success;
        finalScore >= (maxScore * passPercentage / 100) ?
            completion = scorm.set("cmi.core.lesson_status", "passed") :
            completion = scorm.set("cmi.core.lesson_status", "failed");

        // If the course was successfully set to "completed"...
        completion ?
            scorm.quit() :
            console.log("Ошибка: Курс не может быть отмечен как пройденный!");
    } else {
        console.log("Ошибка: Курс не подключён к LMS");
    }
}

function initFinishButton() {
    let completeButton = document.getElementById("complete-button");
    let completeFailureButton = document.getElementById("complete-button-failure");

    if (completeButton) {
        completeButton.addEventListener('click', function onClick(e) {
            e.preventDefault();
            // uploadProgress();
            setComplete();
            completeButton.removeEventListener('click', onClick);
            window.close();
            const course = document.getElementById('course');
            const body = document.querySelector('body');
            const navMenu = document.querySelector('nav.navbar');
            const progressBar = document.querySelector('#progress-bar');
            if(navMenu) {
                navMenu.style.display = 'none';
            }
            if(progressBar) {
                progressBar.style.display = 'none';
            }
            course.style.display = 'none';
            body.insertAdjacentHTML('beforeend', '<div class="container mb-20 text-center" style="margin-top: 400px;">' +
                '<p>Этот материал пройден. Закройте вкладку или переходите к другому материалу.</p>' +
                '</div>');
        });
        if (completeFailureButton) {
            completeFailureButton.addEventListener('click', function onClick(e) {
                e.preventDefault();
                setComplete();
                completeButton.removeEventListener('click', onClick);
                window.close();
                const course = document.getElementById('course');
                const body = document.querySelector('body');
                const navMenu = document.querySelector('nav.navbar');
                const progressBar = document.querySelector('#progress-bar');
                if(navMenu) {
                    navMenu.style.display = 'none';
                }
                if(progressBar) {
                    progressBar.style.display = 'none';
                }
                course.style.display = 'none';
                body.insertAdjacentHTML('beforeend', `
                    <div class="container mb-20 text-center" style="margin-top: 400px;">
                        <p>Этот материал пройден. Закройте вкладку или переходите к другому материалу.</p>
                    </div>
                `);
            });
        }
    }
}


