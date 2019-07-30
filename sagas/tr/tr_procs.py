import grpc

import language_id_pb2 as z_langid
import language_id_pb2_grpc as z_langid_g
import normalization_pb2 as z_normalization
import normalization_pb2_grpc as z_normalization_g
import preprocess_pb2 as z_preprocess
import preprocess_pb2_grpc as z_preprocess_g
import morphology_pb2 as z_morphology
import morphology_pb2_grpc as z_morphology_g

class TrProcs(object):
    def __init__(self):
        channel = grpc.insecure_channel('localhost:6789')

        self.langid_stub = z_langid_g.LanguageIdServiceStub(channel)
        self.normalization_stub = z_normalization_g.NormalizationServiceStub(channel)
        self.preprocess_stub = z_preprocess_g.PreprocessingServiceStub(channel)
        self.morphology_stub = z_morphology_g.MorphologyServiceStub(channel)

    def find_lang_id(self, i):
        response = self.langid_stub.Detect(z_langid.LanguageIdRequest(input=i))
        return response.langId

    def tokenize(self, i):
        response = self.preprocess_stub.Tokenize(z_preprocess.TokenizationRequest(input=i))
        return response.tokens

    def normalize(self, i):
        response = self.normalization_stub.Normalize(z_normalization.NormalizationRequest(input=i))
        return response

    def analyze(self, i):
        response = self.morphology_stub.AnalyzeSentence(z_morphology.SentenceAnalysisRequest(input=i))
        return response

