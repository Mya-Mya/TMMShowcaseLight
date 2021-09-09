//@ts-check
import jQuery from "jquery";
const $ = jQuery;
import tmmData from "../tmmdata_tmmf2n.json";
import {
  type_shelfIds,
  type_shelves,
  type_lessons,
  type_chapters,
  type_medias,
} from "./tmmf2n";

const idName = {
  shelvesList: "#shelves_list",
  shelvesGodown: "#shelves_godown",
  shelfContainer: "#shelf_container",
  shelfGodown: "#shelf_godown",
  shelfName: "#shelf_name",
  lessonsList: "#lessons_list",
  lessonContainer: "#lesson_container",
  lessonName: "#lesson_name",
  chaptersList: "#chapters_list",
};

/**
 * リストアイテムDOMを生成する。
 * @param {string} id
 * @param {string} value
 * @returns {JQuery}
 */
function createActionListItem(id, value) {
  const code = `<div class="list-group-item list-group-item-action" id="${id}">${value}</div>`;
  return $(code);
}
/**
 * 1つのチャプターを表すビューを生成する。
 * @param name {string}
 * @return {JQuery}
 */
function createChapterWrapper(name) {
  const code = `<div class="container-fluid py-2 my-2">
  <h4 class="text-secondary p-3">${name}</h4>
  </div>`;
  return $(code);
}
/**
 * YouTube埋め込みを生成する。
 * @param payload {string}
 * @return {JQuery}
 */
function createYouTubeEmbedding(payload) {
  const code = `<div class="ratio ratio-16x9">
    <iframe src="https://www.youtube.com/embed/${payload}" allowfullscreen></iframe>
    </div>`;
  return $(code);
}

function onDOMReady() {
  $(idName.shelvesGodown).hide();
  $(idName.shelfContainer).hide();
  $(idName.shelfGodown).hide();
  $(idName.lessonContainer).hide();
  //存在するシェルフ名の一覧を表示する。
  /**@type type_shelfIds */
  const shelfIds = tmmData.shelfIds;
  /**@type type_shelves */
  const shelves = tmmData.shelves;
  shelfIds.forEach((shelfId) => {
    const shelf = shelves[shelfId];
    createActionListItem(shelf.id, shelf.name)
      .appendTo(idName.shelvesList)
      .on("click", (_) => onShelfClicked(shelf.id));
  });
}
$(onDOMReady);

/**
 * シェルフが選択された時に呼び出す。
 * そのシェルフが持つレッスン名の一覧を表示する。
 * @param {string} shelfId
 */
function onShelfClicked(shelfId) {
  /**@type type_shelves */
  const shelves = tmmData.shelves;
  /**@type type_lessons */
  const lessons = tmmData.lessons;
  const shelf = shelves[shelfId];

  $(idName.shelfGodown).hide();
  $(idName.lessonContainer).hide();

  $(idName.shelfContainer).show();
  $(idName.shelfName).text(shelf.name);
  $(idName.lessonsList).empty();

  shelf.lessonIds.forEach((lessonId) => {
    const lesson = lessons[lessonId];
    createActionListItem(lessonId, lesson.name)
      .appendTo(idName.lessonsList)
      .on("click", (_) => onLessonClicked(lessonId));
  });

  $(idName.shelvesGodown).show();
}

/**
 * レッスンが選択された時に呼び出す。
 * そのレッスンが持つチャプター及びそれらが持つメディアを表示する。
 * @param {string} lessonId
 */
function onLessonClicked(lessonId) {
  /**@type type_lessons */
  const lessons = tmmData.lessons;
  /**@type type_chapters */
  const chapters = tmmData.chapters;
  /**@type type_medias */
  const medias = tmmData.medias;
  const lesson = lessons[lessonId];

  $(idName.lessonContainer).show();
  $(idName.chaptersList).empty();
  $(idName.lessonName).text(lesson.name);
  lesson.chapterIds.forEach((chapterId) => {
    const chapter = chapters[chapterId];
    const chapterView = createChapterWrapper(chapter.name).appendTo(
      idName.chaptersList
    );
    chapter.mediaIds.forEach((mediaId) => {
      const media = medias[mediaId];
      //メディアタイプが増えたら別のメソッドにまとめ直す
      if (media.type == "youtube") {
        createYouTubeEmbedding(media.payload).appendTo(chapterView);
      }
    });
  });

  $(idName.shelfGodown).show();
}
