/**
 * @typedef {"swipe_left"|"swipe_right"|"pinch_out"|"click"} MTouchEvent
 * @typedef {{[number]: SingleTouchState}} MTouchLayout
 * @callback {} MTouchCallback
*/

class MTouchState {
    /** @type {boolean} */
    enabled;
    /** @type {number} */
    touch_deadzone;
    /** @type {number} */
    off_axis_ratio;
    /** @type {MTouchLayout} */
    touches;
    /** @type {MTouchEvent[]} */
    touch_events;

    /** @type {Function|null} */
    callback;

    constructor() {
        this.enabled = false;
        this.touch_deadzone = 10;
        this.off_axis_ratio = 1.5;
        this.touches = {};
        this.touch_events = [];
        this.callback = null;
    }
}

class Vec2 {
    x = 0;
    y = 0;

    /**
     * @param {number|undefined} x
     * @param {number|undefined} y
     */
    constructor(x, y) {
        this.x = (x === undefined) ? 0 : x;
        this.y = (y === undefined) ? 0 : y;
    }
}

class SingleTouchState {
    /** @type {Vec2} */
    movement;
    /** @type {Vec2} */
    position = new Vec2();

    constructor() {
        this.movement = new Vec2();
        this.position = new Vec2();
    }

    /**
     * @param {MTouchState} state
     * @returns boolean
     */
    isClick(state) {
        return vlen(this.movement) <= state.touch_deadzone;
    }
}

/**
 * @param {Function|undefined} callback_opt
 * @param {HTMLElement|undefined} element_opt
 * @returns {MTouchState}
 */
function initTouchState(callback, element) {
    element = element ? element : document;
    callback = callback ? callback : null;
    let state = new MTouchState();
    state.callback = callback;


    element.addEventListener("touchstart", (evt) => {
        if (state.enabled) {
            for (let i = 0; i < evt.changedTouches.length; i++) {
                let ctouch = evt.changedTouches[i];
                let id = ctouch.identifier;
                state.touches[id] = new SingleTouchState();
                state.touches[id].position = { x: ctouch.pageX, y: ctouch.pageY };
            }
            //evt.preventDefault();
        }
    });
    element.addEventListener("touchmove", (evt) => {
        if (state.enabled) {
            for (let i = 0; i < evt.changedTouches.length; i++) {
                let id = evt.changedTouches[i].identifier;
                let ctouch = evt.changedTouches[i];

                // process touch move 
                let new_pos = new Vec2(ctouch.pageX, ctouch.pageY)
                state.touches[id].movement = vadd(
                    state.touches[id].movement,
                    vsub(new_pos, state.touches[id].position));
                state.touches[id].position = new_pos;
            }
            //evt.preventDefault();
        }
    });
    element.addEventListener("touchend", (evt) => {
        for (let i = 0; i < evt.changedTouches.length; i++) {
            let id = evt.changedTouches[i].identifier;

            // process touch end
            let out_evt = "click";
            {
                if (state.touches[id].isClick(state)) {
                    out_evt = "click";
                } else {
                    let cm = state.touches[id].movement;
                    if (Math.abs(cm.x) > state.off_axis_ratio * Math.abs(cm.y)) {
                        out_evt = (cm.x < 0) ? "swipe_left" : "swipe_right";
                    } else {
                        out_evt = "click"; // Workaround for now
                    }
                }
            }

            if (state.callback !== null) {
                state.callback(out_evt);
            }

            delete state.touches[id];
        }
    });
    element.addEventListener("touchcancel", (evt) => {
        for (let i = 0; i < evt.changedTouches.length; i++) {
            let id = evt.changedTouches[i].identifier;
            delete state.touches[id];
        }
        //evt.preventDefault();
    });
    return state;
}

/**
 * @param {Vec2} a
 * @param {Vec2} b
 * @returns {Vec2}
 */
function vadd(a, b) {
    return new Vec2(a.x + b.x, a.y + b.y);
}

/**
 * @param {Vec2} a
 * @returns {Vec2}
 */
function vneg(a) {
    return new Vec2(- a.x, - a.y);
}

/**
 * @param {Vec2} a
 * @param {Vec2} b
 * @returns {Vec2}
 */
function vsub(a, b) {
    return new Vec2(a.x - b.x, a.y - b.y);
;
}

/**
 * @param {Vec2} v
 * @returns {number}
 */
function vlen_sq(v) {
    return ((v.x * v.x) + (v.y * v.y));
}

/**
 * @param {Vec2} v
 * @returns {number}
 */
function vlen(v) {
    return Math.sqrt(vlen_sq(v))
}
