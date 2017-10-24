var AJAX_SERVER = '/talks/';
var EVENT_UUID = '21e4a4f5-caf5-4086-b7bc-c5b6a0abd68a';

var speakerModalData = {
  title: '',
  titleError: '',
  firstName: '',
  firstNameError: '',
  lastName: '',
  lastNameError: '',
  email: '',
  emailError: '',
  phone: '',
  phoneError: '',
  bio: '',
  bioError: '',
  country: 'SK',
  countryError: '',
  url: '',
  urlError: '',
  socialUrl: '',
  socialUrlError: '',
  image: '',
  imageError: '',
  open: false
};

var talkModalData = {
  talkTitle: '',
  talkTitleError: '',
  talkAbstract: '',
  talkAbstractError: '',
  flag: '',
  flagError: '',
  type: '',
  typeError: '',
  language: '',
  languageError: '',
  duration: '',
  durationError: '',
  optionsData: {
    talk_duration: [
      {text: '30 minutes', value: '30'},
      {text: '45 minutes', value: '45'},
    ],
    workshop_duration: [
      {text: '60 minutes', value: '60'},
      {text: '90 minutes', value: '90'},
      {text: '120 minutes', value: '120'},
      {text: '180 minutes', value: '180'},
      {text: '240 minutes', value: '240'},
    ]
  },
  timeOptions: [],
  open: false
};

var popupModal = new Vue({
  el: '#popupModal',
  data: {
    header: '',
    message: '',
    open: false
  },
  methods: {
    msg: function (message, header) {
      this.header = header;
      this.message = message;
      this.open = true;
    }
  }
});

var speakerModal = new Vue({
  el: '#speakerModal',
  data: speakerModalData,
  computed: {
    validateFirstName: function () {
      if (this.firstName === '') {
        this.firstNameError = 'This field is required!';
      } else {
        this.firstNameError = '';
      }

      return this.firstNameError
    },
    validateLastName: function () {
      if (this.lastName === '') {
        this.lastNameError = 'This field is required!';
      } else {
        this.lastNameError = '';
      }

      return this.lastNameError
    },
    validatePhone: function () {
      if (this.phone === '') {
        this.phoneError = 'This field is required!';
      } else {
        this.phoneError = '';
      }

      return this.phoneError
    },
    validateEmail: function () {
      if (this.email === '') {
        this.emailError = 'This field is required!';
      } else if (this.email.indexOf("@") === -1) {
        this.emailError = 'Wrong email format!';
      } else {
        this.emailError = '';
      }

      return this.emailError
    },
    validateBio: function () {
      if (this.bio === '') {
        this.bioError = 'This field is required!';
      } else {
        this.bioError = '';
      }

      return this.bioError
    },
    collectFormData: function () {
      var formData = new FormData();

      formData.append("event_uuid", EVENT_UUID);
      formData.append("title", talkModal.talkTitle);
      formData.append("abstract", talkModal.talkAbstract);
      formData.append("flag", talkModal.flag);
      formData.append("type", talkModal.type);
      formData.append("language", talkModal.language);
      formData.append("duration", talkModal.duration);

      formData.append("primary_speaker.title", speakerModal.title);
      formData.append("primary_speaker.first_name", speakerModal.firstName);
      formData.append("primary_speaker.last_name", speakerModal.lastName);
      formData.append("primary_speaker.phone", speakerModal.phone);
      formData.append("primary_speaker.email", speakerModal.email);
      formData.append("primary_speaker.bio", speakerModal.bio);
      formData.append("primary_speaker.country", speakerModal.country);
      formData.append("primary_speaker.url", speakerModal.url);
      formData.append("primary_speaker.socialUrl", speakerModal.socialUrl);

      var imagefile = document.querySelector('#avatar');

      if (typeof imagefile.files[0] !== 'undefined') {
        formData.append("primary_speaker.image", imagefile.files[0]);
      }

      return formData
    }
  },
  watch: {
    firstName: function (input) {
      this.validateFirstName;
    },
    lastName: function (input) {
      this.validateLastName;
    },
    phone: function (input) {
      this.validatePhone;
    },
    email: function (input) {
      this.validateEmail;
    },
    bio: function (input) {
      this.validateBio;
    },
    title: function (input) {
      this.titleError = '';
    },
    country: function (input) {
      this.countryError = '';
    },
    url: function (input) {
      this.urlError = '';
    },
    socialUrl: function (input) {
      this.socialUrlError = '';
    },
    image: function (input) {
      this.imageError = '';
    }
  },
  methods: {
    validateForm: function (event) {
      event.preventDefault();

      this.validateFirstName;
      this.validateLastName;
      this.validatePhone;
      this.validateEmail;
      this.validateBio;

      if (!this.titleError && !this.firstNameError && !this.lastNameError && !this.phoneError && !this.emailError
        && !this.bioError && !this.countryError && !this.urlError && !this.socialUrlError) {
        this.ajaxData();
      }
    },
    openPopUp: function (message, header) {
      popupModal.msg(message, header);
      speakerModal.open = false;
      talkModal.open = false;
    },
    ajaxData: function () {
      const config = {headers: {'Content-Type': 'multipart/form-data'}};
      var formData = this.collectFormData;

      axios.post(AJAX_SERVER, formData, config).then(function (response) {
        speakerModal.openPopUp('Your proposal has been submitted.', response.status + ': ' + response.statusText);

      }).catch(function (error) {
        // Something went wrong
        if ('response' in error && typeof error.response !== 'undefined') {

          if (error.response.status === 400) {
            var error_data = error.response.data;
            // Error status indicate wrong input! Update form fields with messages returned from API.
            for (var field in error_data) {

              if (field === 'primary_speaker') {
                for (var ps_field in error_data[field]) {
                  speakerModal[ps_field + 'Error'] = error_data[field][ps_field][0];
                }
              } else {
                speakerModal.open = false; // Close speakerModal so user see error in talkModal
                talkModal[field + 'Error'] = error_data[field][0];
              }

              if (field === 'event_uuid') {
                speakerModal.openPopUp(error_data[field][0], '404: Event NOT FOUND');
              }
            }
          } else if (error.response.status === 404) {
            speakerModal.openPopUp('Server page was not found!', error.response.status + ': ' + error.response.statusText);
          } else if (error.response.status === 500) {
            speakerModal.openPopUp(error.response.statusText, error.response.status + ': ' + error.response.statusText);
          } else {
            // Different error status than wrong input!
            console.log(error.response);
            if ('detail' in error.response.data) {
              speakerModal.openPopUp(error.response.data['detail'], error.response.status + ': ' + error.response.statusText);
            } else {
              speakerModal.openPopUp(error.message, error.response.status + ': ' + error.response.statusText);
            }
          }
        } else {
          speakerModal.openPopUp(error.message);
        }
      });
    }
  }
});

var talkModal = new Vue({
  el: '#talkModal',
  data: talkModalData,
  computed: {
    validateTalkTitle: function () {
      if (this.talkTitle === '') {
        this.talkTitleError = 'This field is required!';
      } else {
        this.talkTitleError = '';
      }

      return this.talkTitleError
    },
    validateTalkAbstract: function () {
      if (this.talkAbstract === '') {
        this.talkAbstractError = 'This field is required!';
      } else {
        this.talkAbstractError = '';
      }

      return this.talkAbstract
    },
    validateFlag: function () {
      if (this.flag === '') {
        this.flagError = 'This field is required!';
      } else {
        this.flagError = '';
      }

      return this.flag
    },
    validateType: function () {
      if (this.type === '') {
        this.typeError = 'This field is required!';
      } else {
        this.typeError = '';
      }

      return this.type
    },
    validateLanguage: function () {
      if (this.language === '') {
        this.languageError = 'This field is required!';
      } else {
        this.languageError = '';
      }

      return this.language
    },
    validateDuration: function () {
      if (this.duration === '') {
        this.durationError = 'This field is required!';
      } else {
        this.durationError = '';
      }

      return this.duration
    },
    changeDuration: function () {

      switch (this.type) {

        case 'talk':
          timeOptions = this.optionsData.talk_duration;
          break;

        case 'workshop':
          timeOptions = this.optionsData.workshop_duration;
          break;

        default:
          timeOptions = this.optionsData.talk_duration;
      }

      return timeOptions
    }
  },
  watch: {
    talkTitle: function (input) {
      this.validateTalkTitle;
    },
    talkAbstract: function (input) {
      this.validateTalkAbstract;
    },
    flag: function (input) {
      this.validateFlag;
    },
    type: function (input) {
      this.validateType;
      this.timeOptions = this.changeDuration
    },
    language: function (input) {
      this.validateLanguage;
    },
    duration: function (input) {
      this.validateDuration;
    }
  },
  methods: {
    validateForm: function (event) {
      this.validateTalkTitle
      this.validateTalkAbstract
      this.validateFlag
      this.validateType
      this.validateLanguage
      this.validateDuration

      if (this.talkTitleError || this.talkAbstractError || this.flagError || this.typeError || this.languageError || this.durationError) {
        event.preventDefault();
      }
    }
  }
});
