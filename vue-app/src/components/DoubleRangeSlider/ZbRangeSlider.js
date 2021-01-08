/* eslint-disable*/

export default function rangeSlider(id) {
  const selfRange = this;
  let startX = 0;
  let x = 0;

  // retrieve touch button
  const slider = document.getElementById(id);
  const touchLeft = slider.querySelector('.slider-touch-left');
  const touchRight = slider.querySelector('.slider-touch-right');
  const lineSpan = slider.querySelector('.slider-line span');

  // get some properties
  let min = parseFloat(slider.getAttribute('se-min'));
  let max = parseFloat(slider.getAttribute('se-max'));

  // retrieve default values
  let defaultMinValue = min;
  if (slider.hasAttribute('se-min-value')) {
    defaultMinValue = parseFloat(slider.getAttribute('se-min-value'));
  }
  let defaultMaxValue = max;

  if (slider.hasAttribute('se-max-value')) {
    defaultMaxValue = parseFloat(slider.getAttribute('se-max-value'));
  }

  // check values are correct
  if (defaultMinValue < min) {
    defaultMinValue = min;
  }

  if (defaultMaxValue > max) {
    defaultMaxValue = max;
  }

  if (defaultMinValue > defaultMaxValue) {
    defaultMinValue = defaultMaxValue;
  }

  let step = 0.0;

  if (slider.getAttribute('se-step')) {
    step = Math.abs(parseFloat(slider.getAttribute('se-step')));
  }

  // normalize flag
  const normalizeFact = 26;

  selfRange.slider = slider;
  selfRange.reset = function reset() {
    touchLeft.style.left = '0px';
    touchRight.style.left = `${slider.offsetWidth - touchLeft.offsetWidth}px`;
    lineSpan.style.marginLeft = '0px';
    lineSpan.style.width = `${slider.offsetWidth - touchLeft.offsetWidth}px`;
    startX = 0;
    x = 0;
  };

  selfRange.setMinThreshold = function setMinThreshold(minThreshold) {
    selfRange.reset();
    min = minThreshold;
  };

  selfRange.setMaxThreshold = function setMaxThreshold(maxThreshold) {
    selfRange.reset();
    max = maxThreshold;
  };

  selfRange.setMinValue = function setMinValue(minValue) {
    const ratio = (minValue - min) / (max - min);
    touchLeft.style.left = `${Math.ceil(
      ratio * (slider.offsetWidth - (touchLeft.offsetWidth + normalizeFact)),
    )}px`;
    lineSpan.style.marginLeft = `${touchLeft.offsetLeft}px`;
    lineSpan.style.width = `${touchRight.offsetLeft - touchLeft.offsetLeft}px`;
    slider.setAttribute('se-min-value', minValue);
  };

  selfRange.setMaxValue = function setMaxValue(maxValue) {
    const ratio = (maxValue - min) / (max - min);
    touchRight.style.left = `${Math.ceil(
      ratio * (slider.offsetWidth - (touchLeft.offsetWidth + normalizeFact))
          + normalizeFact,
    )}px`;
    lineSpan.style.marginLeft = `${touchLeft.offsetLeft}px`;
    lineSpan.style.width = `${touchRight.offsetLeft - touchLeft.offsetLeft}px`;
    slider.setAttribute('se-max-value', maxValue);
  };

  // initial reset
  selfRange.reset();

  // usefull values, min, max, normalize fact is the width of both touch buttons
  const maxX = slider.offsetWidth - touchRight.offsetWidth;
  let selectedTouch = null;
  const initialValue = lineSpan.offsetWidth - normalizeFact;

  // set defualt values
  selfRange.setMinValue(defaultMinValue);
  selfRange.setMaxValue(defaultMaxValue);

  // setup touch/click events
  function onStart(event) {
    // Prevent default dragging of selected content
    event.preventDefault();
    let eventTouch = event;

    if (event.touches) {
      eventTouch = event.touches[0];
    }

    if (this === touchLeft) {
      x = touchLeft.offsetLeft;
    } else {
      x = touchRight.offsetLeft;
    }

    startX = eventTouch.pageX - x;
    selectedTouch = this;
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onStop);
    document.addEventListener('touchmove', onMove);
    document.addEventListener('touchend', onStop);
  }

  function onMove(event) {
    let eventTouch = event;

    if (event.touches) {
      eventTouch = event.touches[0];
    }

    x = eventTouch.pageX - startX;

    if (selectedTouch === touchLeft) {
      if (x > touchRight.offsetLeft - selectedTouch.offsetWidth + 10) {
        x = touchRight.offsetLeft - selectedTouch.offsetWidth + 10;
      } else if (x < 0) {
        x = 0;
      }

      selectedTouch.style.left = `${x}px`;
    } else if (selectedTouch === touchRight) {
      if (x < touchLeft.offsetLeft + touchLeft.offsetWidth - 10) {
        x = touchLeft.offsetLeft + touchLeft.offsetWidth - 10;
      } else if (x > maxX) {
        x = maxX;
      }
      selectedTouch.style.left = `${x}px`;
    }

    // update line span
    lineSpan.style.marginLeft = `${touchLeft.offsetLeft}px`;
    lineSpan.style.width = `${touchRight.offsetLeft - touchLeft.offsetLeft}px`;

    // write new value
    calculateValue();

    // call on change
    if (slider.getAttribute('on-change')) {
      const fn = new Function('min, max', slider.getAttribute('on-change'));
      fn(
        slider.getAttribute('se-min-value'),
        slider.getAttribute('se-max-value'),
      );
    }

    if (selfRange.onChange) {
      selfRange.onChange(
        slider.getAttribute('se-min-value'),
        slider.getAttribute('se-max-value'),
      );
    }
  }

  function onStop() {
    document.removeEventListener('mousemove', onMove);
    document.removeEventListener('mouseup', onStop);
    document.removeEventListener('touchmove', onMove);
    document.removeEventListener('touchend', onStop);

    selectedTouch = null;

    // write new value
    calculateValue();

    // call did changed
    if (slider.getAttribute('did-changed')) {
      const fn = new Function('min, max', slider.getAttribute('did-changed'));
      fn(
        slider.getAttribute('se-min-value'),
        slider.getAttribute('se-max-value'),
      );
    }

    if (selfRange.didChanged) {
      selfRange.didChanged(
        slider.getAttribute('se-min-value'),
        slider.getAttribute('se-max-value'),
      );
    }
  }

  function calculateValue() {
    const newValue = (lineSpan.offsetWidth - normalizeFact) / initialValue;
    let minValue = lineSpan.offsetLeft / initialValue;
    let maxValue = minValue + newValue;

    minValue = minValue * (max - min) + min;
    maxValue = maxValue * (max - min) + min;

    if (step !== 0.0) {
      let multi = Math.floor(minValue / step);
      minValue = step * multi;

      multi = Math.floor(maxValue / step);
      maxValue = step * multi;
    }

    slider.setAttribute('se-min-value', minValue);
    slider.setAttribute('se-max-value', maxValue);
  }

  // link events
  touchLeft.addEventListener('mousedown', onStart);
  touchRight.addEventListener('mousedown', onStart);
  touchLeft.addEventListener('touchstart', onStart);
  touchRight.addEventListener('touchstart', onStart);

  let isWider = false;
  window.addEventListener('resize', () => {
    if (window.matchMedia('(max-width: 1200px)').matches) {
      if (!isWider) {
        selfRange.reset();
        // console.log("Thinker than 1200");
        isWider = true;
      }
    } else if (isWider) {
      selfRange.reset();
      // console.log("Wider than 1200");
      isWider = false;
    }
  });
}
