import modeling


def main():

    # this is the order of the arguments ---> run_model(num_of_epochs, train_size, test_size, batch_Size, model_number, filters, dropout, model_number)

    print("-----------------------------------------------------------------")
    print("------------------------------------------------------------------")
    print("model 99:")
    modeling.run_model(num_of_epochs=20, train_size=82620, test_size=27540, batch_Size=280, filters=8, dropout=0.1, kernel=7, model_number=99)


if __name__ == '__main__':
        main()
