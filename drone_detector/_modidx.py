# Autogenerated by nbdev

d = { 'settings': { 'audience': 'Developers',
                'author': 'Janne Mäyrä',
                'author_email': 'janne.mayra@syke.fi',
                'branch': 'master',
                'console_scripts': 'predict_segmentation_fastai=drone_detector.engines.fastaipredict:predict_segmentation_fastai\n'
                                   'predict_bboxes_icevision=drone_detector.engines.icevision.predict:predict_bboxes_icevision\n'
                                   'predict_bboxes_detectron2=drone_detector.engines.detectron2.predict:predict_bboxes_detectron2\n'
                                   'predict_instance_masks_detectron2=drone_detector.engines.detectron2.predict:predict_instance_masks_detectron2',
                'copyright': 'Janne Mäyrä',
                'custom_sidebar': 'True',
                'description': 'Automated deadwood detection from UAV RGB imagery',
                'doc_baseurl': '/drone_detector/',
                'doc_host': 'https://mayrajeo.github.io',
                'doc_path': '_docs',
                'git_url': 'https://github.com/mayrajeo/drone_detector/tree/master/',
                'host': 'github',
                'keywords': 'UAV Imagery, object detection',
                'language': 'English',
                'lib_name': 'drone_detector',
                'lib_path': 'drone_detector',
                'license': 'apache2',
                'min_python': '3.8',
                'nbs_path': 'nbs',
                'recursive': 'False',
                'status': '2',
                'title': 'drone_detector',
                'tst_flags': 'examples',
                'user': 'mayrajeo',
                'version': '0.0.1'},
  'syms': { 'drone_detector.engines.detectron2.augmentations': { 'drone_detector.engines.detectron2.augmentations.T.RotationTransform.apply_rotated_box': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.augmentations.html#t.rotationtransform.apply_rotated_box',
                                                                 'drone_detector.engines.detectron2.augmentations.VFlip_rotated_box': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.augmentations.html#vflip_rotated_box',
                                                                 'drone_detector.engines.detectron2.augmentations.build_aug_transforms': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.augmentations.html#build_aug_transforms'},
            'drone_detector.engines.detectron2.predict': { 'drone_detector.engines.detectron2.predict.predict_bboxes': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.predict.html#predict_bboxes',
                                                           'drone_detector.engines.detectron2.predict.predict_bboxes_detectron2': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.predict.html#predict_bboxes_detectron2',
                                                           'drone_detector.engines.detectron2.predict.predict_instance_masks': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.predict.html#predict_instance_masks',
                                                           'drone_detector.engines.detectron2.predict.predict_instance_masks_detectron2': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.predict.html#predict_instance_masks_detectron2'},
            'drone_detector.engines.detectron2.training': { 'drone_detector.engines.detectron2.training.RotatedDatasetMapper': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.training.html#rotateddatasetmapper',
                                                            'drone_detector.engines.detectron2.training.RotatedTrainer': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.training.html#rotatedtrainer',
                                                            'drone_detector.engines.detectron2.training.RotatedTrainer.build_evaluator': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.training.html#rotatedtrainer.build_evaluator',
                                                            'drone_detector.engines.detectron2.training.RotatedTrainer.build_train_loader': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.training.html#rotatedtrainer.build_train_loader',
                                                            'drone_detector.engines.detectron2.training.Trainer': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.training.html#trainer',
                                                            'drone_detector.engines.detectron2.training.Trainer.build_evaluator': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.training.html#trainer.build_evaluator',
                                                            'drone_detector.engines.detectron2.training.Trainer.build_train_loader': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.training.html#trainer.build_train_loader',
                                                            'drone_detector.engines.detectron2.training.transform_rotated_annotations': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.training.html#transform_rotated_annotations'},
            'drone_detector.engines.detectron2.tta': { 'drone_detector.engines.detectron2.tta.DatasetMapperTTAFlip': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.tta.html#datasetmapperttaflip',
                                                       'drone_detector.engines.detectron2.tta.DatasetMapperTTAFlip.from_config': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.tta.html#datasetmapperttaflip.from_config',
                                                       'drone_detector.engines.detectron2.tta.GeneralizedRCNNWithTTA._get_augmented_boxes': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.tta.html#generalizedrcnnwithtta._get_augmented_boxes',
                                                       'drone_detector.engines.detectron2.tta.GeneralizedRCNNWithTTA._merge_detections': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.tta.html#generalizedrcnnwithtta._merge_detections',
                                                       'drone_detector.engines.detectron2.tta.GeneralizedRCNNWithTTA._reduce_pred_masks': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.tta.html#generalizedrcnnwithtta._reduce_pred_masks',
                                                       'drone_detector.engines.detectron2.tta.GeneralizedRCNNWithTTA._rescale_detected_boxes': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.tta.html#generalizedrcnnwithtta._rescale_detected_boxes',
                                                       'drone_detector.engines.detectron2.tta.TTAPredictor': 'https://mayrajeo.github.io/drone_detector/engines.detectron2.tta.html#ttapredictor'},
            'drone_detector.engines.fastai.augmentations': { 'drone_detector.engines.fastai.augmentations.AlbumentationsTransform': 'https://mayrajeo.github.io/drone_detector/engines.fastai.augmentations.html#albumentationstransform',
                                                             'drone_detector.engines.fastai.augmentations.AlbumentationsTransform.before_call': 'https://mayrajeo.github.io/drone_detector/engines.fastai.augmentations.html#albumentationstransform.before_call',
                                                             'drone_detector.engines.fastai.augmentations.AlbumentationsTransform.encodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.augmentations.html#albumentationstransform.encodes',
                                                             'drone_detector.engines.fastai.augmentations.RegressionMask.affine_coord': 'https://mayrajeo.github.io/drone_detector/engines.fastai.augmentations.html#regressionmask.affine_coord',
                                                             'drone_detector.engines.fastai.augmentations.SegmentationAlbumentationsTransform': 'https://mayrajeo.github.io/drone_detector/engines.fastai.augmentations.html#segmentationalbumentationstransform',
                                                             'drone_detector.engines.fastai.augmentations.SegmentationAlbumentationsTransform.encodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.augmentations.html#segmentationalbumentationstransform.encodes'},
            'drone_detector.engines.fastai.data': { 'drone_detector.engines.fastai.data.MultiChannelImageBlock': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimageblock',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders.from_csv': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders.from_csv',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders.from_df': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders.from_df',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders.from_folder': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders.from_folder',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders.from_lists': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders.from_lists',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders.from_name_func': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders.from_name_func',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders.from_name_re': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders.from_name_re',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders.from_path_func': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders.from_path_func',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders.from_path_re': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders.from_path_re',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageDataLoaders.from_shapefile': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagedataloaders.from_shapefile',
                                                    'drone_detector.engines.fastai.data.MultiChannelImageTupleBlock': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichannelimagetupleblock',
                                                    'drone_detector.engines.fastai.data.MultiChannelTensorImage': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichanneltensorimage',
                                                    'drone_detector.engines.fastai.data.MultiChannelTensorImage.create': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichanneltensorimage.create',
                                                    'drone_detector.engines.fastai.data.MultiChannelTensorImage.show': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichanneltensorimage.show',
                                                    'drone_detector.engines.fastai.data.MultiChannelTensorImageTuple': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichanneltensorimagetuple',
                                                    'drone_detector.engines.fastai.data.MultiChannelTensorImageTuple.create': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichanneltensorimagetuple.create',
                                                    'drone_detector.engines.fastai.data.MultiChannelTensorImageTuple.show': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#multichanneltensorimagetuple.show',
                                                    'drone_detector.engines.fastai.data.RegressionMask': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#regressionmask',
                                                    'drone_detector.engines.fastai.data.RegressionMask.create': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#regressionmask.create',
                                                    'drone_detector.engines.fastai.data.RegressionMask.show': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#regressionmask.show',
                                                    'drone_detector.engines.fastai.data.RegressionMaskBlock': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#regressionmaskblock',
                                                    'drone_detector.engines.fastai.data.ScaleToFloatTensor': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#scaletofloattensor',
                                                    'drone_detector.engines.fastai.data.ScaleToFloatTensor.decodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#scaletofloattensor.decodes',
                                                    'drone_detector.engines.fastai.data.ScaleToFloatTensor.encodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#scaletofloattensor.encodes',
                                                    'drone_detector.engines.fastai.data.TifSegmentationDataLoaders': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#tifsegmentationdataloaders',
                                                    'drone_detector.engines.fastai.data.TifSegmentationDataLoaders.from_label_func': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#tifsegmentationdataloaders.from_label_func',
                                                    'drone_detector.engines.fastai.data.get_all_but_last': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#get_all_but_last',
                                                    'drone_detector.engines.fastai.data.get_image_timeseries': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#get_image_timeseries',
                                                    'drone_detector.engines.fastai.data.get_last': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#get_last',
                                                    'drone_detector.engines.fastai.data.label_from_different_folder': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#label_from_different_folder',
                                                    'drone_detector.engines.fastai.data.label_with_matching_fname': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#label_with_matching_fname',
                                                    'drone_detector.engines.fastai.data.norm': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#norm',
                                                    'drone_detector.engines.fastai.data.open_geotiff': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#open_geotiff',
                                                    'drone_detector.engines.fastai.data.open_npy': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#open_npy',
                                                    'drone_detector.engines.fastai.data.show_batch': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#show_batch',
                                                    'drone_detector.engines.fastai.data.show_composite': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#show_composite',
                                                    'drone_detector.engines.fastai.data.show_mean_spectra': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#show_mean_spectra',
                                                    'drone_detector.engines.fastai.data.show_normalized_spectral_index': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#show_normalized_spectral_index',
                                                    'drone_detector.engines.fastai.data.show_results': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#show_results',
                                                    'drone_detector.engines.fastai.data.show_single_channel': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#show_single_channel',
                                                    'drone_detector.engines.fastai.data.using_attr': 'https://mayrajeo.github.io/drone_detector/engines.fastai.data.html#using_attr'},
            'drone_detector.engines.fastai.losses': { 'drone_detector.engines.fastai.losses.FocalDice': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#focaldice',
                                                      'drone_detector.engines.fastai.losses.FocalDice.activation': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#focaldice.activation',
                                                      'drone_detector.engines.fastai.losses.FocalDice.decodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#focaldice.decodes',
                                                      'drone_detector.engines.fastai.losses.LovaszHingeLoss': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszhingeloss',
                                                      'drone_detector.engines.fastai.losses.LovaszHingeLoss.activation': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszhingeloss.activation',
                                                      'drone_detector.engines.fastai.losses.LovaszHingeLoss.decodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszhingeloss.decodes',
                                                      'drone_detector.engines.fastai.losses.LovaszHingeLoss.forward': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszhingeloss.forward',
                                                      'drone_detector.engines.fastai.losses.LovaszHingeLossFlat': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszhingelossflat',
                                                      'drone_detector.engines.fastai.losses.LovaszHingeLossFlat.activation': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszhingelossflat.activation',
                                                      'drone_detector.engines.fastai.losses.LovaszHingeLossFlat.decodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszhingelossflat.decodes',
                                                      'drone_detector.engines.fastai.losses.LovaszSigmoidLoss': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsigmoidloss',
                                                      'drone_detector.engines.fastai.losses.LovaszSigmoidLoss.activation': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsigmoidloss.activation',
                                                      'drone_detector.engines.fastai.losses.LovaszSigmoidLoss.decodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsigmoidloss.decodes',
                                                      'drone_detector.engines.fastai.losses.LovaszSigmoidLoss.forward': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsigmoidloss.forward',
                                                      'drone_detector.engines.fastai.losses.LovaszSigmoidLossFlat': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsigmoidlossflat',
                                                      'drone_detector.engines.fastai.losses.LovaszSigmoidLossFlat.activation': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsigmoidlossflat.activation',
                                                      'drone_detector.engines.fastai.losses.LovaszSigmoidLossFlat.decodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsigmoidlossflat.decodes',
                                                      'drone_detector.engines.fastai.losses.LovaszSoftmaxLoss': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsoftmaxloss',
                                                      'drone_detector.engines.fastai.losses.LovaszSoftmaxLoss.activation': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsoftmaxloss.activation',
                                                      'drone_detector.engines.fastai.losses.LovaszSoftmaxLoss.decodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsoftmaxloss.decodes',
                                                      'drone_detector.engines.fastai.losses.LovaszSoftmaxLoss.forward': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsoftmaxloss.forward',
                                                      'drone_detector.engines.fastai.losses.LovaszSoftmaxLossFlat': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsoftmaxlossflat',
                                                      'drone_detector.engines.fastai.losses.LovaszSoftmaxLossFlat.activation': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsoftmaxlossflat.activation',
                                                      'drone_detector.engines.fastai.losses.LovaszSoftmaxLossFlat.decodes': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovaszsoftmaxlossflat.decodes',
                                                      'drone_detector.engines.fastai.losses.flatten_binary_scores': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#flatten_binary_scores',
                                                      'drone_detector.engines.fastai.losses.flatten_probas': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#flatten_probas',
                                                      'drone_detector.engines.fastai.losses.iou': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#iou',
                                                      'drone_detector.engines.fastai.losses.iou_binary': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#iou_binary',
                                                      'drone_detector.engines.fastai.losses.isnan': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#isnan',
                                                      'drone_detector.engines.fastai.losses.lovasz_grad': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovasz_grad',
                                                      'drone_detector.engines.fastai.losses.lovasz_hinge': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovasz_hinge',
                                                      'drone_detector.engines.fastai.losses.lovasz_hinge_flat': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovasz_hinge_flat',
                                                      'drone_detector.engines.fastai.losses.lovasz_softmax': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovasz_softmax',
                                                      'drone_detector.engines.fastai.losses.lovasz_softmax_flat': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#lovasz_softmax_flat',
                                                      'drone_detector.engines.fastai.losses.mean': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#mean',
                                                      'drone_detector.engines.fastai.losses.xloss': 'https://mayrajeo.github.io/drone_detector/engines.fastai.losses.html#xloss'},
            'drone_detector.engines.fastai.predict': { 'drone_detector.engines.fastai.predict.DataLoader.set_base_transforms': 'https://mayrajeo.github.io/drone_detector/engines.fastai.predict.html#dataloader.set_base_transforms',
                                                       'drone_detector.engines.fastai.predict.Pipeline.remove': 'https://mayrajeo.github.io/drone_detector/engines.fastai.predict.html#pipeline.remove',
                                                       'drone_detector.engines.fastai.predict.predict_segmentation': 'https://mayrajeo.github.io/drone_detector/engines.fastai.predict.html#predict_segmentation',
                                                       'drone_detector.engines.fastai.predict.predict_segmentation_fastai': 'https://mayrajeo.github.io/drone_detector/engines.fastai.predict.html#predict_segmentation_fastai'},
            'drone_detector.imports': {},
            'drone_detector.metrics': { 'drone_detector.metrics.GisCOCOeval': 'https://mayrajeo.github.io/drone_detector/metrics.html#giscocoeval',
                                        'drone_detector.metrics.GisCOCOeval.evaluate': 'https://mayrajeo.github.io/drone_detector/metrics.html#giscocoeval.evaluate',
                                        'drone_detector.metrics.GisCOCOeval.prepare_data': 'https://mayrajeo.github.io/drone_detector/metrics.html#giscocoeval.prepare_data',
                                        'drone_detector.metrics.GisCOCOeval.prepare_eval': 'https://mayrajeo.github.io/drone_detector/metrics.html#giscocoeval.prepare_eval',
                                        'drone_detector.metrics.GisCOCOeval.save_results': 'https://mayrajeo.github.io/drone_detector/metrics.html#giscocoeval.save_results',
                                        'drone_detector.metrics.JaccardCoeffMulti': 'https://mayrajeo.github.io/drone_detector/metrics.html#jaccardcoeffmulti',
                                        'drone_detector.metrics.JaccardCoeffMulti.value': 'https://mayrajeo.github.io/drone_detector/metrics.html#jaccardcoeffmulti.value',
                                        'drone_detector.metrics.adjusted_R2Score': 'https://mayrajeo.github.io/drone_detector/metrics.html#adjusted_r2score',
                                        'drone_detector.metrics.average_precision': 'https://mayrajeo.github.io/drone_detector/metrics.html#average_precision',
                                        'drone_detector.metrics.average_recall': 'https://mayrajeo.github.io/drone_detector/metrics.html#average_recall',
                                        'drone_detector.metrics.bias': 'https://mayrajeo.github.io/drone_detector/metrics.html#bias',
                                        'drone_detector.metrics.bias_pct': 'https://mayrajeo.github.io/drone_detector/metrics.html#bias_pct',
                                        'drone_detector.metrics.coverage_error': 'https://mayrajeo.github.io/drone_detector/metrics.html#coverage_error',
                                        'drone_detector.metrics.is_false_positive': 'https://mayrajeo.github.io/drone_detector/metrics.html#is_false_positive',
                                        'drone_detector.metrics.is_true_positive': 'https://mayrajeo.github.io/drone_detector/metrics.html#is_true_positive',
                                        'drone_detector.metrics.label_ranking_average_precision_score': 'https://mayrajeo.github.io/drone_detector/metrics.html#label_ranking_average_precision_score',
                                        'drone_detector.metrics.label_ranking_loss': 'https://mayrajeo.github.io/drone_detector/metrics.html#label_ranking_loss',
                                        'drone_detector.metrics.one_error': 'https://mayrajeo.github.io/drone_detector/metrics.html#one_error',
                                        'drone_detector.metrics.poly_IoU': 'https://mayrajeo.github.io/drone_detector/metrics.html#poly_iou',
                                        'drone_detector.metrics.poly_dice': 'https://mayrajeo.github.io/drone_detector/metrics.html#poly_dice',
                                        'drone_detector.metrics.rrmse': 'https://mayrajeo.github.io/drone_detector/metrics.html#rrmse'},
            'drone_detector.processing.all': {},
            'drone_detector.processing.coco': { 'drone_detector.processing.coco.COCOProcessor': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#cocoprocessor',
                                                'drone_detector.processing.coco.COCOProcessor.coco_to_shp': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#cocoprocessor.coco_to_shp',
                                                'drone_detector.processing.coco.COCOProcessor.results_to_coco_res': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#cocoprocessor.results_to_coco_res',
                                                'drone_detector.processing.coco.COCOProcessor.shp_to_coco': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#cocoprocessor.shp_to_coco',
                                                'drone_detector.processing.coco.binary_mask_to_polygon': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#binary_mask_to_polygon',
                                                'drone_detector.processing.coco.calc_bearing': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#calc_bearing',
                                                'drone_detector.processing.coco.close_contour': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#close_contour',
                                                'drone_detector.processing.coco.detectron2_bbox_preds_to_coco_anns': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#detectron2_bbox_preds_to_coco_anns',
                                                'drone_detector.processing.coco.detectron2_mask_preds_to_coco_anns': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#detectron2_mask_preds_to_coco_anns',
                                                'drone_detector.processing.coco.nor_theta': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#nor_theta',
                                                'drone_detector.processing.coco.resize_binary_mask': 'https://mayrajeo.github.io/drone_detector/processing.coco.html#resize_binary_mask'},
            'drone_detector.processing.coordinates': { 'drone_detector.processing.coordinates.affine_transform_gdf': 'https://mayrajeo.github.io/drone_detector/processing.coordinates.html#affine_transform_gdf',
                                                       'drone_detector.processing.coordinates.convert_poly_coords': 'https://mayrajeo.github.io/drone_detector/processing.coordinates.html#convert_poly_coords',
                                                       'drone_detector.processing.coordinates.gdf_to_px': 'https://mayrajeo.github.io/drone_detector/processing.coordinates.html#gdf_to_px',
                                                       'drone_detector.processing.coordinates.georegister_px_df': 'https://mayrajeo.github.io/drone_detector/processing.coordinates.html#georegister_px_df'},
            'drone_detector.processing.postproc': { 'drone_detector.processing.postproc.bb_intersection_over_union': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#bb_intersection_over_union',
                                                    'drone_detector.processing.postproc.denormalize_bbox_coords': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#denormalize_bbox_coords',
                                                    'drone_detector.processing.postproc.dilate_erode': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#dilate_erode',
                                                    'drone_detector.processing.postproc.do_min_rot_rectangle_nms': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#do_min_rot_rectangle_nms',
                                                    'drone_detector.processing.postproc.do_nms': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#do_nms',
                                                    'drone_detector.processing.postproc.do_poly_nms': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#do_poly_nms',
                                                    'drone_detector.processing.postproc.do_wbf': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#do_wbf',
                                                    'drone_detector.processing.postproc.do_wsf': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#do_wsf',
                                                    'drone_detector.processing.postproc.fill_holes': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#fill_holes',
                                                    'drone_detector.processing.postproc.find_matching_box_quickly': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#find_matching_box_quickly',
                                                    'drone_detector.processing.postproc.get_weighted_box': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#get_weighted_box',
                                                    'drone_detector.processing.postproc.non_max_suppression_fast': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#non_max_suppression_fast',
                                                    'drone_detector.processing.postproc.non_max_suppression_poly': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#non_max_suppression_poly',
                                                    'drone_detector.processing.postproc.normalize_bbox_coords': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#normalize_bbox_coords',
                                                    'drone_detector.processing.postproc.prefilter_boxes': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#prefilter_boxes',
                                                    'drone_detector.processing.postproc.weighted_boxes_fusion': 'https://mayrajeo.github.io/drone_detector/processing.postproc.html#weighted_boxes_fusion'},
            'drone_detector.processing.tiling': { 'drone_detector.processing.tiling.Tiler': 'https://mayrajeo.github.io/drone_detector/processing.tiling.html#tiler',
                                                  'drone_detector.processing.tiling.Tiler.tile_and_rasterize_vector': 'https://mayrajeo.github.io/drone_detector/processing.tiling.html#tiler.tile_and_rasterize_vector',
                                                  'drone_detector.processing.tiling.Tiler.tile_raster': 'https://mayrajeo.github.io/drone_detector/processing.tiling.html#tiler.tile_raster',
                                                  'drone_detector.processing.tiling.Tiler.tile_vector': 'https://mayrajeo.github.io/drone_detector/processing.tiling.html#tiler.tile_vector',
                                                  'drone_detector.processing.tiling.copy_sum': 'https://mayrajeo.github.io/drone_detector/processing.tiling.html#copy_sum',
                                                  'drone_detector.processing.tiling.untile_raster': 'https://mayrajeo.github.io/drone_detector/processing.tiling.html#untile_raster',
                                                  'drone_detector.processing.tiling.untile_vector': 'https://mayrajeo.github.io/drone_detector/processing.tiling.html#untile_vector'},
            'drone_detector.utils': { 'drone_detector.utils.cone_v': 'https://mayrajeo.github.io/drone_detector/utils.html#cone_v',
                                      'drone_detector.utils.cut_cone_v': 'https://mayrajeo.github.io/drone_detector/utils.html#cut_cone_v',
                                      'drone_detector.utils.fix_multipolys': 'https://mayrajeo.github.io/drone_detector/utils.html#fix_multipolys',
                                      'drone_detector.utils.rangeof': 'https://mayrajeo.github.io/drone_detector/utils.html#rangeof'}}}