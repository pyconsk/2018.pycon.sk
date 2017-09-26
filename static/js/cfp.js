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
  avatar: '',
  avatarError: ''
};

var talkModalData = {
  talkTitle: '',
  talkTitleError: '',
  talkAbstract: '',
  talkAbstractError: '',
  type: 'TALK',
  typeError: '',
  language: 'EN',
  languageError: '',
  duration: 30,
  durationError: ''
};

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
  },
  methods: {
    validateForm: function (event) {
      this.validateFirstName;
      this.validateLastName;
      this.validatePhone;
      this.validateEmail;
      this.validateBio;

      if (this.titleError || this.firstNameError || this.lastNameError || this.phoneError || this.emailError
        || this.bioError || this.countryError || this.urlError || this.socialUrlError || this.avatarError) {
        event.preventDefault();
      }
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
    collectJSONData: function () {
      var data = {
        speaker_title: speakerModal.title,
        first_name: speakerModal.firstName,
        last_name: speakerModal.lastName,
        phone: speakerModal.phone,
        email: speakerModal.email,
        bio: speakerModal.bio,
        country: speakerModal.country,
        url: speakerModal.url,
        socialUrl: speakerModal.socialUrl,
        image: speakerModal.avatar,
        title: this.talkTitle,
        'abstract': this.talkAbstract,
        type: this.type,
        language: this.language,
        duration: this.duration
      };
      return JSON.stringify(data)
    }
  },
  watch: {
    talkTitle: function (input) {
      this.validateTalkTitle;
    },
    talkAbstract: function (input) {
      this.validateTalkAbstract;
    }
  },
  methods: {
    ajaxData: function () {
      // TODO: Finish once backend is up!
      var payload = this.collectJSONData;
      console.log(payload);

      axios.post('/TODO', {data: payload})
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          // Something went wrong
          console.log(error.message);

          // TODO: Set error, messages from backend!

          talkModal.titleError = 'This field is required!';
          speakerModal.firstNameError = 'This field is required!';
          talkModal.$refs.modal_2.click(); // hide talk modal if there is error in speaker modal
        });
    },
    validateForm: function (event) {
      event.preventDefault();  // Do not submit, we want AJAX post on backend.

      this.validateTalkTitle
      this.validateTalkAbstract
      if (!this.talkTitleError || !this.talkAbstractError || !this.typeError || !this.languageError || !this.durationError) {
        this.ajaxData();
      }
    }
  }
});
