// sleep time expects milliseconds
function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}


class VoiceRecorder {
    constructor() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            console.log("getUserMedia supported")
        } else {
            console.log("getUserMedia is not supported on your browser!")
        }

        this.mediaRecorder
        this.stream
        this.chunks = []
        this.isRecording = false
        this.send_to_server = true

        this.recorderRef = document.querySelector("#recording #recorder");
        this.playerRef = document.querySelector("#recording #player");
        this.startRef = document.querySelector("#recording #start");
        this.stopRef = document.querySelector("#stop_recording");
        this.disablerecordRef = document.querySelector("#recording #disablerecord");
        this.blob = null;
        this.sendLogoRef = document.querySelector("#sendLogo");
        this.msg_inputRef = document.querySelector("#msg_input");
        this.recording_counter = document.querySelector("#recording_counter");

        this.startRef.onclick = this.startRecording.bind(this)
        this.stopRef.onclick = this.stopRecording.bind(this)
        this.disablerecordRef.onclick = this.disablerecording.bind(this)

        this.minutesLabel = document.querySelector("#recording_counter #minutes");
        this.secondsLabel = document.querySelector("#recording_counter #seconds");

        this.constraints = {
            audio: true,
            video: false
        }


    }

    handleSuccess(stream) {
        this.stream = stream
        this.stream.oninactive = () => {
            console.log("Stream ended!")
        };
        this.recorderRef.srcObject = this.stream
        this.mediaRecorder = new MediaRecorder(this.stream)
        this.mediaRecorder.ondataavailable = this.onMediaRecorderDataAvailable.bind(this)
        this.mediaRecorder.onstop = this.onMediaRecorderStop.bind(this)
        this.recorderRef.play()
        this.startRef.style.display = 'none';
        this.disablerecordRef.style.display = 'block';
        this.stopRef.style.display = 'block';
        this.sendLogoRef.style.display = 'none';
        this.msg_inputRef.setAttribute('disabled', 'disabled');
        this.msg_inputRef.value = '';
        this.recording_counter.style.display = 'block';
        this.msg_inputRef.style.display = 'none';
        window.totalSeconds = 0;

        // Play This tune when starts recording.
        let start_voice_message_tune_obj = new Audio(start_voice_message_tune)
        start_voice_message_tune_obj.play();

        window.totalSeconds = 0;
        this.time_interval = setInterval(setTime, 1000);

        function setTime() {
            if (window.totalSeconds >= 59) {
                voiceRecorder.stopRef.click();
            } else {
                ++window.totalSeconds;
                voiceRecorder.secondsLabel.innerHTML = pad(window.totalSeconds % 60);
                voiceRecorder.minutesLabel.innerHTML = pad(parseInt(window.totalSeconds / 60), true);
            }
        }

        function pad(val, min = false) {
            var valString = val + "";
            if (valString.length < 2) {
                if (min) {
                    return valString;
                } else {
                    return "0" + valString;
                }
            } else {
                return valString;
            }
        }


        sleep(490).then(() => {
            this.mediaRecorder.start()
    });
        




    }

    handleError(error) {
        console.log("navigator.getUserMedia error: ", error)
    }

    onMediaRecorderDataAvailable(e) { this.chunks.push(e.data)
         console.log(e.data) }

    onMediaRecorderStop() {
        this.stream.getAudioTracks().forEach(track => track.stop())
        this.stream = null
        const blob = new Blob(this.chunks, { 'type': 'audio/mp3;' })
        this.blob = blob;
        const audioURL = window.URL.createObjectURL(blob)
        this.playerRef.src = audioURL
        this.chunks = []


        if (this.send_to_server) {
            this.sendRecordtoServer();
        } else {
            window.totalSeconds = 0;
        }



    }

    startRecording() {

        if (this.isRecording) return
        this.isRecording = true
        this.playerRef.src = ''
        navigator.mediaDevices
            .getUserMedia(this.constraints)
            .then(this.handleSuccess.bind(this))
            .catch(this.handleError.bind(this))

        this.secondsLabel.innerHTML = "00";
        this.minutesLabel.innerHTML = "0";
        clearInterval(this.time_interval);

    }

    stopRecording() {
        this.send_to_server = true;
        this.startRef.style.display = 'block';
        this.disablerecordRef.style.display = 'none';
        this.stopRef.style.display = 'none';
        this.sendLogoRef.style.display = 'block';
        this.msg_inputRef.removeAttribute('disabled');
        this.msg_inputRef.value = '';
        this.recording_counter.style.display = 'none';
        this.msg_inputRef.style.display = 'block';

        this.playerRef.src = ''
        if (!this.isRecording) return
        this.isRecording = false
        this.recorderRef.pause()
        this.mediaRecorder.stop()


        this.secondsLabel.innerHTML = "00";
        this.minutesLabel.innerHTML = "0";
        clearInterval(this.time_interval);

    }


    disablerecording() {
        this.send_to_server = false;

        if (!this.isRecording) return
        this.isRecording = false
        this.recorderRef.pause()
        this.mediaRecorder.stop()

        this.startRef.style.display = 'block';
        this.disablerecordRef.style.display = 'none';
        this.stopRef.style.display = 'none';
        this.playerRef.src = ''
        this.sendLogoRef.style.display = 'block';
        this.msg_inputRef.removeAttribute('disabled');
        this.msg_inputRef.value = '';
        this.msg_inputRef.style.display = 'block';
        this.recording_counter.style.display = 'none';

        window.totalSeconds = 0;
        this.secondsLabel.innerHTML = "00";
        this.minutesLabel.innerHTML = "0";
        clearInterval(this.time_interval);

    }

    sendRecordtoServer() {

        var fd = new FormData();
        fd.append('fname', 'audio.mp3');
        fd.append('data', this.blob);
        fd.append('duration', window.totalSeconds + 1);

        $.ajax({
            type: 'POST',
            url: record_voice_api + "/" + $("#current_user").text(),
            data: fd,
            processData: false,
            contentType: false,


            success: function (msg) {
                const msgs = msg.new_msg;
                if (msgs.to_user_id == $("#current_user").text() && msgs.from_user_id == request_user_id) {
                    $('#Messages_List').append('<div class="chat-msg owner" data-msgid="' + msgs.id + '"><div class="chat-msg-profile"><div class="chat-msg-date"><span data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></span><span data-seen="' + msgs.seen + '"></span></div></div><audio class="voicerecord_audio" data-duration="' + msgs.voice_file_duration + '" style="display: block;" preload="auto" controls hidden><source src="/media' + msgs.voice_file + '"></audio></div>');

                    getSeen(document.querySelectorAll("[data-seen]"));
                    getDate(document.querySelectorAll('[data-dateid="' + msgs.id + '"]'));
                    loadAudioDesign('[data-msgid="' + msgs.id + '"] .voicerecord_audio');

                    // Scroll Dwon When New Message Received
                    $('#chat-area').animate({ scrollTop: $('#chat-area').prop("scrollHeight") }, 500);

                    // Update Friends List

                    // Add New Message To Conversation Area and Freind Area
                    var element = document.querySelector('[data-freinduserid="' + msgs.friend_id + '"]');
                    if (element != null) {
                        element.remove();
                    }

                    if (msgs.msg.length != 0) {
                        $('#conversation-area-js').prepend('<a onclick="reloadChatArea(' + msgs.friend_id + ')" id="conversation-area-friend-Link" data-freindUserid="' + msgs.friend_id + '"><div class="msg" data-userid="' + msgs.friend_id + '"><img class="msg-profile" src="' + msgs.friend_profile_picture + '" alt=""><div class="msg-detail"><div class="msg-username">' + msgs.friend_name + '</div><div class="msg-content"><span class="msg-message">' + msgs.msg + '</span><span class="msg-date" data-friendid="' + msgs.friend_id + '" data-dateconv="' + msgs.date_utc + '"></span></div></div></div></a>');
                        countUpFromFriendAreaMessages(msgs.friend_id);
                    }

                    let new_msg_elment = document.querySelector('[data-userid="' + msgs.friend_id + '"]')


                    if ($("#current_user").text() == msgs.friend_id && $(".active").length == 0) {
                        new_msg_elment.classList.add('active');
                    }
                    if (msgs.seen == false && $('#current_user').text() != msgs.friend_id) {
                        new_msg_elment.classList.add('online');
                    }

                }
            }

        })
    }

}



window.voiceRecorder = new VoiceRecorder();