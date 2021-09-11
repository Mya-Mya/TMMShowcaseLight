//@ts-check
import jQuery from "jquery";
const $ = jQuery;
/**
 * @param {string} type
 * @param {string} payload
 * @returns {JQuery}
 */
function createMediaView(type, payload) {
  let code = ``;
  if (type === "youtube") {
    code = `<div class="ratio ratio-16x9">
    <iframe src="https://www.youtube.com/embed/${payload}" allowfullscreen></iframe>
    </div>`;
  }
  return $(code);
}

export default createMediaView;
