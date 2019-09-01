/*

 jQuery Markdown editor
 derived from https://github.com/digitalnature/MarkdownEditor
 and https://github.com/jamiebicknell/Markdown-Helper
*/
;(function ($, window, document, undefined) {
    $.fn.MarkdownEditor = function () {

        var adjustOffset = function (input, offset) {
                let val = input.value, newOffset = offset;

                // adjust starting offset, because some browsers (like Opera) treat new lines as two characters (\r\n) instead of one character (\n)
                if (val.indexOf("\r\n") > -1) {
                    let matches = val.replace(/\r\n/g, "\n").slice(0, offset).match(/\n/g);
                    newOffset += matches ? matches.length : 0;
                }

                return newOffset;
            },

            // creates a selection inside the textarea
            // if selectionStart = selectionEnd the cursor is set to that point
            setCaretToPos = function (input, selectionStart, selectionEnd) {
                input.focus();

                if (input.setSelectionRange) {
                    input.setSelectionRange(adjustOffset(input, selectionStart), adjustOffset(input, selectionEnd));

                    // ie
                } else if (input.createTextRange) {
                    let range = input.createTextRange();
                    range.collapse(true);
                    range.moveEnd('character', selectionEnd);
                    range.moveStart('character', selectionStart);
                    range.select();
                }
            },

            // indents the textarea selection
            indent = function (textArea, prefix, count) {

                // extend the selection start until the previous line feed
                let selection, newValue, range = {
                    start: textArea.value.lastIndexOf('\n', textArea.selectionStart),
                    end: textArea.selectionEnd
                };

                // if there isn't a line feed before,
                // then extend the selection until the begging of the text
                if (range.start === -1)
                    range.start = 0;

                // if the selection ends with a line feed,
                // remove it from the selection
                if (textArea.value.charAt(range.end - 1) === '\n')
                    range.end -= 1;

                // extend the selection end until the next line feed
                range.end = textArea.value.indexOf('\n', range.end);

                // if there isn't a line feed after,
                // then extend the selection end until the end of the text
                if (range.end === -1)
                    range.end = textArea.value.length;

                // move the selection to a new variable
                selection = '\n' + textArea.value.substring(range.start, range.end) + '\n\n';

                newValue = textArea.value.substring(0, range.start);
                newValue += selection.replace(/^(?=.+)/mg, Array(count + 1).join(prefix));  // add 'count' spaces before line feeds
                newValue += textArea.value.substring(range.end);

                textArea.value = newValue;
            },

            tags = {
                bold: {start: '**', end: '**', placeholder: 'Your bold text'},
                italic: {start: '*', end: '*', placeholder: 'Your emphasized text'},
                link: {start: '[', end: '](N)', placeholder: 'Add your link title'},
                head: {start: '#', end: '', placeholder: 'Your header'},
                image: {start: '![', end: '](N)', placeholder: 'Add image description'},
                pre: {start: '', end: '', placeholder: '\n' + '    Add your code block here' + '\n'},
                code: {start: '`', end: '`', placeholder: 'Add inline code here'},
                ul: {start: '* ', end: '', placeholder: 'List Item'},
                ol: {start: '1. ', end: '', placeholder: 'List Item'},
            };

        return this.each(function () {
            let txt = this,                          // textarea element
                controls = $('<div class="controls" id="'+txt.id+'-controls" />'); // button container

            const format_classes = "btn btn-light";
            const button_template = '<button type="button" data-toggle="tooltip" data-placement="bottom" title="';
            $(txt).before(controls.append(
                '<div class="btn-toolbar" role="toolbar" aria-label="Markdown Toolbar">'
                + '<div class="btn-group mr-2 mb-1" role="group" aria-label="Formatting">'
                + button_template + 'Bold" class="' + format_classes + ' c-bold"><i class="fas fa-bold"></i></button>'
                + button_template + 'Italic" class="' + format_classes + ' c-italic"><i class="fas fa-italic"></i></button>'
                + button_template + 'Heading" class="' + format_classes + ' c-head"><i class="fas fa-heading"></i></button>'
                + button_template + 'Code" class="' + format_classes + ' c-code"><i class="fas fa-code"></i></button>'
                + '</div><div class="btn-group mr-2 mb-1" role="group" aria-label="Utilities">'
                + button_template + 'Link" class="' + format_classes + ' c-link"><i class="fas fa-link"></i></button>'
                + button_template + 'Image" class="' + format_classes + ' c-image"><i class="fas fa-image"></i></button>'
                + '</div><div class="btn-group mr-2 mb-1" role="group" aria-label="Lists">'
                + button_template + 'Bullet List" class="' + format_classes + ' c-ul"><i class="fas fa-list-ul"></i></button>'
                + button_template + 'Ordered List" class="' + format_classes + ' c-ol"><i class="fas fa-list-ol"></i></button>'
                + '</div>' +
                '</div>'
            ));

            $(txt).on('keypress', function (event) {
                return MarkdownHelper(txt, event);
            });

            $('button', controls).on('click', function (event) {
                event.preventDefault();
                txt.focus();

                let tagName = this.className.substr(format_classes.length + 3),
                    range = {start: txt.selectionStart, end: txt.selectionEnd};

                //head should instead affect the whole line
                if (['head', 'ul','ol'].includes(tagName)) {
                    let linestart = txt.value.lastIndexOf('\n', range.start) + 1,
                        lineend = txt.value.indexOf('\n', range.end) - 1;
                    lineend = lineend === -2 ? range.end : lineend;
                    range = {start: linestart, end: lineend};
                }

                let selectedText = txt.value.substring(range.start, range.end),
                    adjacent_characters_to_selected_text = $.trim(txt.value.charAt(range.start - 1) + txt.value.charAt(range.end));

                // if this is a code tag, decide if it needs to go inline or inside a block
                tagName = (tagName === 'code') && ((selectedText.indexOf('\n') !== -1) || (!adjacent_characters_to_selected_text) || (txt.value.length < 1)) ? 'pre' : tagName;

                let tag = $.extend({}, tags[tagName]),
                    trimmed_placeholder = $.trim(tag.placeholder),
                    number_of_spaces_removed_from_placeholder = tag.placeholder.indexOf(trimmed_placeholder);

                // do nothing if the selection text matches the placeholder text
                if (selectedText === trimmed_placeholder)
                    return true;

                // handle link/image requests
                if ($.inArray(tagName, ['link', 'image']) !== -1) {
                    let url = prompt((tagName !== 'image') ? 'Enter the URL' : 'Enter image URL', 'http://');

                    if (url) {
                        tag.end = tag.end.replace('N', url);
                    } else {
                        return true;
                    }
                }

                // no actual text selection or text selection matches default placeholder text
                if (range.start === range.end) {
                    txt.value = txt.value.substring(0, range.end) + tag.start + tag.placeholder + tag.end + txt.value.substring(range.end);
                    setCaretToPos(txt, range.end + tag.start.length + number_of_spaces_removed_from_placeholder, range.end + tag.start.length + number_of_spaces_removed_from_placeholder + trimmed_placeholder.length);

                    // we have selected text
                } else {
                    // code blocks require indenting only
                    if (tagName === 'pre')
                        indent(txt, ' ', 4);

                    // the others need to wrapped between tags
                    else
                        txt.value = txt.value.replace(selectedText, tag.start + selectedText + tag.end);

                }

                return true;
            });

        });

    };

})(jQuery, window, document);

function MarkdownHelper(block, event) {
    let check, input, start, range, lines, state, value, first, prior, label, begin, width, caret;
    if (event.keyCode === 13) {
        check = false;
        input = block.value.replace(/\r\n/g, '\n');
        if (block.selectionStart) {
            start = block.selectionStart;
        } else {
            block.focus();
            range = document.selection.createRange();
            range.moveStart('character', -input.length);
            start = range.text.replace(/\r\n/g, '\n').length;
        }
        lines = input.split('\n');
        state = input.substr(0, start).split('\n').length;
        value = lines[state - 1].replace(/^\s+/, '');
        first = value.substr(0, 2);
        if (new RegExp('^[0-9]+[.] (.*)$').test(value)) {
            prior = value.substr(0, value.indexOf('. '));
            begin = prior + '. ';
            label = (parseInt(prior, 10) + 1) + '. ';
            check = true;
        }
        if (value && !check && lines[state - 1].substr(0, 4) === '    ') {
            begin = label = '    ';
            check = true;
        }
        if (['* ', '+ ', '- '].indexOf(first) >= 0) {
            begin = label = first;
            check = true;
        }
        if (check) {
            width = lines[state - 1].indexOf(begin);
            if (value.replace(/^\s+/, '') === begin) {
                block.value = input.substr(0, start - 1 - width - label.length) + '\n\n' + input.substr(start, input.length);
                caret = start + 1 - label.length - width;
            } else {
                block.value = input.substr(0, start) + '\n' + (new Array(width + 1).join(' ')) + label + input.substr(start, input.length);
                caret = start + 1 + label.length + width;
            }
            if (block.selectionStart) {
                block.setSelectionRange(caret, caret);
            } else {
                range = block.createTextRange();
                range.move('character', caret);
                range.select();
            }
            return false;
        }
    }
}