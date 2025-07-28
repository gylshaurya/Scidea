const scroller = document.getElementById('tagScroller');
const scrollWrapper = scroller.parentElement;
const left = document.getElementById('scrollLeft');
const right = document.getElementById('scrollRight');

  scroller.addEventListener('scroll', () => {
    left.classList.toggle('hidden', scroller.scrollLeft === 0);
    if (scroller.scrollLeft > 5) {
    scrollWrapper.classList.add('show-left-fade');
    }
    else {
    scrollWrapper.classList.remove('show-left-fade');
    }

    const atEnd = scroller.scrollLeft + scroller.offsetWidth >= scroller.scrollWidth - 5;
    right.classList.toggle('hidden', atEnd);
    if (atEnd) {
      scrollWrapper.classList.add('hide-right-fade');
    } else {
      scrollWrapper.classList.remove('hide-right-fade');
  }

  });

  right.addEventListener('click', () => {
    scroller.scrollBy({ left: 350, behavior: 'smooth' });
  });

  left.addEventListener('click', () => {
    scroller.scrollBy({ left: -350, behavior: 'smooth' });
  });


window.addEventListener('scroll', function() {
    const indicator = document.getElementById('scrollIndicator');
    if (window.scrollY > 10 && indicator) {
      indicator.classList.add('hidden');
    }
  }, { once: true });