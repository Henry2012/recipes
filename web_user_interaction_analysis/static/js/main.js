var helpers = {
  windowHeight : 0,
  adjustDynamicHeightElements : function (){
    //$(".dynamic-height").css({
    //  "height" : helpers.windowHeight-10
   // });
    
  },
  fadeInSplash : function(){
    $(".splash-container .bg").fadeIn(400);
    $(".splash-container .content").fadeIn(1600);
  },
  
  setupCompanyPage: function(){
    $(".face-link").click(function(){
      var self = this;
      var modal =  $(self).attr("href");
      var name = $("h3", self).html();
      var text = $("p", self).html();
      var imgSrc = $(".profile", self).attr('src');
      $(modal + " h2").html( name );
      $(modal + " p").html( text );
      $(".face-banner .modal-body").css({
        "background-image" : "url('" + imgSrc + "')"
      });
      var modalHeight = $(modal + " .text").height();
      $(modal + " .text").css({
        "margin-top": -modalHeight + "px"
      });
    });

    $(".advisor-link").click(function(e){
      e.preventDefault();
      var self = this;
      var div = $(self).parent().parent();
      var row = $(".row", div).clone();
      $("#textModal .container .row").remove();
      $("#textModal .container").append(row);
    });

    $(".read").click(function(e){
      e.preventDefault();
      $(".letter").slideDown();
    });
  },
  setupContactPage: function(){

    $('input, textarea').placeholder();

    var map;
    var mapOptions = {
      zoom: 10,
      center: new google.maps.LatLng(37.55, -122.38),
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      backgroundColor: "#1C1C1C",
      panControl: false,
      zoomControl: true,
      zoomControlOptions: {
        style: google.maps.ZoomControlStyle.MEDIUM,
        position: google.maps.ControlPosition.LEFT_CENTER
      },
      scaleControl: false,
      mapTypeControl: false,
      scrollwheel: false,
      streetViewControl: false,
      styles: [{
        featureType: "water",
        stylers: [{
          color: "#1C1C1C"
        }, {
          visibility: "on"
        }]
      }, {
        featureType: "landscape",
        stylers: [{
          color: "#282828"
        }]
      }, {
        featureType: "administrative",
        elementType: "geometry.stroke",
        stylers: [{
          color: "#4a4a4a"
        }, {
          weight: 0.4
        }]
      }, {
        featureType: "poi",
        stylers: [{
          color: "#3f3f3f"
        }]
      }, {
        featureType: "road",
        elementType: "geometry.fill",
        stylers: [{
          color: "#494949"
        }]
      }, {
        featureType: "road",
        elementType: "geometry.stroke",
        stylers: [{
          color: "#a0a0a0"
        }, {
          weight: 0.1
        }, {
          visibility: "off"
        }]
      }, {
        featureType: "road",
        elementType: "labels.text.stroke",
        stylers: [{
          color: "#282828"
        }, {
          weight: 4
        }]
      }, {
        featureType: "road",
        elementType: "labels.text",
        stylers: [{
          color: "#eaeaea"
        }, {
          weight: 0.5
        }]
      }, {
        elementType: "labels.text",
        stylers: [{
          color: "#dbdbdb"
        }, {
          weight: 0.4
        }]
      }, {
        featureType: "administrative",
        elementType: "labels.text",
        stylers: [{
          visibility: "on"
        }, {
          weight: 0.4
        }, {
          color: "#f9f9f9"
        }]
      }, {
        featureType: "road.highway",
        elementType: "geometry",
        stylers: [{
          color: "#757575"
        }]
      }, {
        featureType: "road",
        elementType: "labels.icon",
        stylers: [{
          visibility: "off"
        }]
      }, {
        featureType: "transit",
        elementType: "labels.icon",
        stylers: [{
          visibility: "off"
        }]
      }, {
        featureType: "transit.station.airport",
        elementType: "geometry",
        stylers: [{
          visibility: "on"
        }, {
          color: "#555555"
        }]
      }, {
        featureType: "administrative",
        elementType: "labels.icon",
        stylers: [{
          visibility: "off"
        }]
      }, {
        featureType: "poi",
        elementType: "labels.icon",
        stylers: [{
          visibility: "off"
        }]
      }, {
        featureType: "transit.line",
        elementType: "geometry",
        stylers: [{
          visibility: "on"
        }, {
          color: "#a0a0a0"
        }]
      }, {
        featureType: "poi.medical",
        elementType: "labels",
        stylers: [{
          color: "#636363"
        }, {
          visibility: "off"
        }]
      }, {
        featureType: "poi.place_of_worship",
        elementType: "labels",
        stylers: [{
          visibility: "off"
        }]
      }, {
        featureType: "poi.attraction",
        elementType: "labels",
        stylers: [{
          visibility: "off"
        }]
      }, {
        featureType: "poi.business",
        elementType: "labels",
        stylers: [{
          visibility: "off"
        }]
      }]
    };

    map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

    var image = '../img/icons/addepar-googlemaps.png';
    var myLatLng = new google.maps.LatLng(37.408183, -122.078924);
    var AddeMarker = new google.maps.Marker({
      position: myLatLng,
      map: map,
      icon: image,
      title: "Addepar"
    });
  }
};

!function ($) {

  $(function(){
    helpers.windowHeight = $(window).height();

    // Scrolling
    $.localScroll();

    var $window = $(window);

    // Disable certain links in docs
    $('section [href^=#]').click(function (e) {
      e.preventDefault();
    });

    // side bar
    $('.side-navigation').affix({
      offset: {
        top: function () { return $(window).width() <= 980 ? 290 : 560; },
        bottom: 700
      }
    });

  });

}(window.jQuery);


$(window).resize(function() {
  helpers.adjustDynamicHeightElements();
  
});