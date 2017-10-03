var AJAX_SERVER = '/talks/';
var EVENT_UUID = '0b66b975-e018-478e-8253-524af072eaed';

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
  type: 'talk',
  typeError: '',
  language: 'EN',
  languageError: '',
  duration: 30,
  durationError: '',
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
    msg: function(message, header) {
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
      formData.append("primary_speaker.image", imagefile.files[0]);

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
        && !this.bioError && !this.countryError && !this.urlError && !this.socialUrlError && !this.imageError) {
        this.ajaxData();
      }
    },
    openPopUp: function (message, header) {
        popupModal.msg(message, header);
        speakerModal.open = false;
        talkModal.open = false;
    },
    ajaxData: function () {
      var formData = this.collectFormData;

      axios.post(AJAX_SERVER, formData).then(function (response) {
        speakerModal.openPopUp('Your proposal has been submitted.', response.status +': '+ response.statusText);

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
            }
          } else if (error.response.status === 500)  {
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
    }
  },
  watch: {
    talkTitle: function (input) {
      this.validateTalkTitle;
    },
    talkAbstract: function (input) {
      this.validateTalkAbstract;
    },
    type: function (input) {
      this.typeError = '';
    },
    language: function (input) {
      this.languageError = '';
    },
    duration: function (input) {
      this.durationError = '';
    }
  },
  methods: {
    validateForm: function (event) {
      this.validateTalkTitle
      this.validateTalkAbstract

      if (this.talkTitleError || this.talkAbstractError || this.typeError || this.languageError || this.durationError) {
        event.preventDefault();
      }
    }
  }
});
