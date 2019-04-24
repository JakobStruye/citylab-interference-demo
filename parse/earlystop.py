from keras.callbacks import EarlyStopping # use as base class

class EarlyStop(EarlyStopping):
    def __init__(self, threshold, min_epochs, **kwargs):
        super(EarlyStop, self).__init__(monitor='loss', **kwargs)
        self.threshold = threshold # threshold for validation loss
        self.min_epochs = min_epochs # min number of epochs to run

    def on_epoch_end(self, epoch, logs=None):
        print(logs)
        print(self.monitor)
        current = logs.get(self.monitor)
        if current is None:
            print("Oeioei niet goed")
            return

        # implement your own logic here
        print("epoch", epoch, "minep", self.min_epochs, "cur", current, "thresh", self.threshold)
        if (epoch >= self.min_epochs) & (current <= self.threshold):
            print("bigstop")
            self.stopped_epoch = epoch
            self.model.stop_training = True
