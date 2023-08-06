;;; bmt.el --- ckclr's BookMarkTree -*- lexical-binding: t -*-
;;; Commentary:
;;; Code:

;; elisp call bookmark to visual studio
(defun ckclr/bmt-bm2v()
  (interactive)
  (let ((file-path (buffer-file-name))
	(repo-sha (org-entry-get 0 "SHA"))
	(head-id (org-entry-get nil "ID")))
    (shell-command (concat "python d:/bmt/bmt_bm2v.py " file-path " " repo-sha " " head-id))))

(provide 'bmt)
;;; bmt.el ends here
