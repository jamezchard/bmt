;;; bmt.el --- ckclr's BookMarkTree -*- lexical-binding: t -*-
;;; Commentary:
;;; Code:

;; elisp call bookmark to visual studio
(defun ckclr/bmt-bm2v()
  (interactive)
  (let ((head-id (org-entry-get nil "ID")))
    (message head-id)
    (shell-command (concat "python d:/bmt/bmt_bm2v.py " head-id))))

(provide 'bmt.el)
;;; bmt.el ends here
