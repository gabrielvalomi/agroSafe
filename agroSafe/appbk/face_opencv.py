"""
Comparação de rosto com OpenCV: detecção Haar + histograma da região da face.
Não usa FastAPI nem serviços externos; adequado para protótipo e testes de fluxo.
"""
from __future__ import annotations

import os
from typing import BinaryIO

import cv2
import numpy as np
from django.conf import settings


def _cascade_path() -> str:
	return os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')


def _largest_face_roi(gray: np.ndarray) -> np.ndarray | None:
	cc = cv2.CascadeClassifier(_cascade_path())
	faces = cc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))
	if len(faces) == 0:
		return None
	x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
	return gray[y : y + h, x : x + w]


def _face_from_bgr(bgr: np.ndarray) -> np.ndarray | None:
	if bgr is None or bgr.size == 0:
		return None
	gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
	gray = cv2.equalizeHist(gray)
	return _largest_face_roi(gray)


def _read_bgr_from_path(path: str) -> np.ndarray | None:
	img = cv2.imread(path, cv2.IMREAD_COLOR)
	return img


def _read_bgr_from_upload(file_obj: BinaryIO) -> np.ndarray | None:
	raw = file_obj.read()
	if not raw:
		return None
	arr = np.frombuffer(raw, dtype=np.uint8)
	return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def _histogram_correlation(face_a: np.ndarray, face_b: np.ndarray) -> float:
	a = cv2.resize(face_a, (128, 128), interpolation=cv2.INTER_AREA)
	b = cv2.resize(face_b, (128, 128), interpolation=cv2.INTER_AREA)
	h1 = cv2.calcHist([a], [0], None, [64], [0, 256])
	h2 = cv2.calcHist([b], [0], None, [64], [0, 256])
	cv2.normalize(h1, h1)
	cv2.normalize(h2, h2)
	return float(cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL))


def comparar_rosto_arquivo_referencia(
	referencia_abs_path: str,
	upload_file: BinaryIO,
	threshold: float | None = None,
) -> tuple[bool, float, str]:
	"""
	Retorna (bate_com_cadastro, correlação, mensagem_curta).
	"""
	th = threshold if threshold is not None else getattr(settings, 'FACE_MATCH_HIST_THRESHOLD', 0.55)
	ref = _read_bgr_from_path(referencia_abs_path)
	if ref is None:
		return False, 0.0, 'referencia_invalida'

	upload_file.seek(0)
	cap = _read_bgr_from_upload(upload_file)
	if cap is None:
		return False, 0.0, 'foto_captura_invalida'

	f1 = _face_from_bgr(ref)
	f2 = _face_from_bgr(cap)
	if f1 is None:
		return False, 0.0, 'sem_rosto_referencia'
	if f2 is None:
		return False, 0.0, 'sem_rosto_captura'

	score = _histogram_correlation(f1, f2)
	ok = score >= th
	msg = 'match' if ok else 'nao_match'
	return ok, score, msg
