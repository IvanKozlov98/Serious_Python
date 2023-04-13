from easy import main_easy
from medium import main_medium

if __name__ == '__main__':
    # main_easy()
    #########################################
    # entry has next fields:
    #   "price"
    #   "location"
    #   "name"
    #   "description"
    #   "url"
    main_medium("Сноуборд 167", filtered_function=lambda x: "46" in x["description"])
