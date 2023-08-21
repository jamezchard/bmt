;;; bmt.el --- ckclr's BookMarkTree -*- lexical-binding: t -*-
;;; Commentary:
;;; Code:

;; elisp call bookmark to visual studio
(defun ckclr/bmt-bm2v()
  (interactive)
  (let ((file-path (buffer-file-name))
	(mark-id (word-at-point)))
    (shell-command (concat "python d:/bmt/bmt_bm2v.py " file-path " " mark-id))
    (message mark-id)))

(provide 'bmt)
;;; bmt.el ends here
