/*
Copyright (c) 2003-2009, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{
	config.language = 'pl';
	config.toolbar = 'Basic';

	config.toolbar_Basic =
		[
		    ['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink'],
		    ['-','Outdent','Indent','Blockquote'],
		    ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock']
		];
};
