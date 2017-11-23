var AJAX_SERVER = 'https://2018.pycon.sk';
var AJAX_URL = AJAX_SERVER + '/tickets/aid/';

function get_event_uuid(slug) {
  axios.get(AJAX_SERVER + '/events/' + slug).then(function (response) {
    return response.data.uuid;
  }).catch(function (error) {
    aidModal.openPopUp(error, 'Could not connect to server!');
    console.log(error);
  });
}

var EVENT_UUID = get_event_uuid('2018');

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

var aidModalData = {
  typeUuid: 'd94fa3ef-76c1-428f-ba26-b172907ee7b0',
  title: '',
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  description: '',
  open: false
};

var aidModal = new Vue({
  el: '#aidModal',
  data: aidModalData,
  computed: {
    collectFormData: function () {
      var formData = new FormData();

      formData.append("type_uuid", this.typeUuid);
      formData.append("title", this.title);
      formData.append("first_name", this.firstName);
      formData.append("last_name", this.lastName);
      formData.append("phone", this.phone);
      formData.append("email", this.email);
      formData.append("description", this.description);

      return formData
    }
  },
  methods: {
    openPopUp: function (message, header) {
      popupModal.msg(message, header);
      aidModal.open = false;
    },
    validateForm: function (event) {
      event.preventDefault();
      this.ajaxData();
      this.open = false;
    },
    ajaxData: function () {
      var formData = this.collectFormData;

      axios.post(AJAX_URL, formData).then(function (response) {
        console.log('Done');
        aidModal.openPopUp('Your request has been submitted.', response.status + ': ' + response.statusText);
      }).catch(function (error) {
        console.log('Error');
        console.log(error);
      });
    },
    addListeners: function() {
      const inputs = document.querySelectorAll("input, select, textarea");

      inputs.forEach(input => {
        input.addEventListener("invalid", event => {
          input.classList.add("error");
          },
          false
        );
      });
    }
  },
  created: function() {
    this.addListeners();
  }
});
