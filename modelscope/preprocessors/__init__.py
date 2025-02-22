# Copyright (c) Alibaba, Inc. and its affiliates.
from typing import TYPE_CHECKING

from modelscope.utils.import_utils import LazyImportModule

if TYPE_CHECKING:
    from .base import Preprocessor
    from .builder import PREPROCESSORS, build_preprocessor
    from .common import Compose, ToTensor, Filter
    from .asr import WavToScp
    from .audio import LinearAECAndFbank
    from .image import (LoadImage, load_image,
                        ImageColorEnhanceFinetunePreprocessor,
                        ImageInstanceSegmentationPreprocessor,
                        ImageDenoisePreprocessor)
    from .kws import WavToLists
    from .tts import KanttsDataPreprocessor
    from .multi_modal import (OfaPreprocessor, MPlugPreprocessor)
    from .nlp import (
        DocumentSegmentationTransformersPreprocessor,
        FaqQuestionAnsweringTransformersPreprocessor,
        FillMaskPoNetPreprocessor, FillMaskTransformersPreprocessor,
        TextRankingTransformersPreprocessor,
        RelationExtractionTransformersPreprocessor,
        SentenceEmbeddingTransformersPreprocessor,
        TextClassificationTransformersPreprocessor,
        TokenClassificationTransformersPreprocessor,
        TextErrorCorrectionPreprocessor, TextGenerationT5Preprocessor,
        TextGenerationTransformersPreprocessor, Tokenize,
        WordSegmentationBlankSetToLabelPreprocessor, CodeGeeXPreprocessor,
        MGLMSummarizationPreprocessor,
        ZeroShotClassificationTransformersPreprocessor,
        TextGenerationJiebaPreprocessor, SentencePiecePreprocessor,
        DialogIntentPredictionPreprocessor, DialogModelingPreprocessor,
        DialogStateTrackingPreprocessor, ConversationalTextToSqlPreprocessor,
        TableQuestionAnsweringPreprocessor, NERPreprocessorViet,
        NERPreprocessorThai, WordSegmentationPreprocessorThai,
        TranslationEvaluationPreprocessor)
    from .video import ReadVideoData, MovieSceneSegmentationPreprocessor

else:
    _import_structure = {
        'base': ['Preprocessor'],
        'builder': ['PREPROCESSORS', 'build_preprocessor'],
        'common': ['Compose', 'ToTensor', 'Filter'],
        'audio': ['LinearAECAndFbank'],
        'asr': ['WavToScp'],
        'video': ['ReadVideoData', 'MovieSceneSegmentationPreprocessor'],
        'image': [
            'LoadImage', 'load_image', 'ImageColorEnhanceFinetunePreprocessor',
            'ImageInstanceSegmentationPreprocessor', 'ImageDenoisePreprocessor'
        ],
        'kws': ['WavToLists'],
        'tts': ['KanttsDataPreprocessor'],
        'multi_modal': ['OfaPreprocessor', 'MPlugPreprocessor'],
        'nlp': [
            'DocumentSegmentationTransformersPreprocessor',
            'FaqQuestionAnsweringTransformersPreprocessor',
            'FillMaskPoNetPreprocessor', 'FillMaskTransformersPreprocessor',
            'NLPTokenizerPreprocessorBase',
            'TextRankingTransformersPreprocessor',
            'RelationExtractionTransformersPreprocessor',
            'SentenceEmbeddingTransformersPreprocessor',
            'TextClassificationTransformersPreprocessor',
            'TokenClassificationTransformersPreprocessor',
            'TextErrorCorrectionPreprocessor',
            'TextGenerationTransformersPreprocessor', 'Tokenize',
            'TextGenerationT5Preprocessor',
            'WordSegmentationBlankSetToLabelPreprocessor',
            'MGLMSummarizationPreprocessor', 'CodeGeeXPreprocessor',
            'ZeroShotClassificationTransformersPreprocessor',
            'TextGenerationJiebaPreprocessor', 'SentencePiecePreprocessor',
            'NERPreprocessorViet', 'NERPreprocessorThai',
            'WordSegmentationPreprocessorThai',
            'DialogIntentPredictionPreprocessor', 'DialogModelingPreprocessor',
            'DialogStateTrackingPreprocessor',
            'ConversationalTextToSqlPreprocessor',
            'TableQuestionAnsweringPreprocessor',
            'TranslationEvaluationPreprocessor'
        ],
    }

    import sys

    sys.modules[__name__] = LazyImportModule(
        __name__,
        globals()['__file__'],
        _import_structure,
        module_spec=__spec__,
        extra_objects={},
    )
