import $ from 'jquery';
class MobileMenu {
  constructor() {
    this.menuIcon        = $('.primary-nav__menu-icon');
    this.menuContent     = $('.primary-nav__menu-content');
    this.dropDownMenu    = $('.primary-nav__dropdown');
    this.dropDownMenuBtn = $('.primary-nav__dropdown__btn');
    this.dropDownMenuBtn = this.dropDownMenuBtn.slice(0,3);
    this.events();
  }

  events() {
    this.menuIcon.click(this.toggleTheMenu.bind(this));
    let that = this;
    this.dropDownMenuBtn.each(function() {
      $(this).click(function() {
        let classID = $(this)[0]["id"];
        that.removeDropDownSubmenu(classID);
        $(this)[0].nextElementSibling.classList.toggle("primary-nav__dropdown-content--is-visible");
      });
    });
  }

  removeDropDownSubmenu(classID) {
    this.dropDownMenuBtn.each(function() {
      let hasThisClassName = "";
      let numOfClassName   = $(this)[0].nextElementSibling.classList.length;
      if (numOfClassName>1) {
        hasThisClassName = $(this)[0].nextElementSibling.classList[1];
      }
      if (hasThisClassName) {
        if ($(this)[0]["id"]!==classID) {
          $(this)[0].nextElementSibling.classList.remove("primary-nav__dropdown-content--is-visible");
        }
      }
    });
  }

  toggleTheMenu() {
    this.dropDownMenu.toggleClass("primary-nav__dropdown--is-visible");
    this.menuContent.toggleClass("primary-nav__menu-content--is-visible");
    this.menuIcon.toggleClass("primary-nav__menu-icon--close-x");
  }
}

export default MobileMenu;
