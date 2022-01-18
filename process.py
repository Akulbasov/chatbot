class Process:

    def __init__(self, intent, parameters):
        self.intent = intent
        self.params = parameters

    __main_template = \
        "<h3>Header</h3><br>" + \
        "Content<br>"

    __df_field = __main_template \
        .replace("Header", "Dialogflow response")

    __sql_field = __main_template \
        .replace("Header", "SQL")

    __result_field = __main_template \
        .replace("Header", "Result")

    @staticmethod
    def __get_parameters_from_protobuf(prbuffstr):
        response_by_new_line = prbuffstr.split("\n")
        end_result_parameters = []
        counter = 0
        key = ""
        value = ""

        for each_line in response_by_new_line:
            if "key: " in each_line and "unit-currency" not in each_line:
                counter += 1
                key = each_line.replace(" ", "").replace("key:", "").replace("\"", "")

            if "string_value: " in each_line:
                counter += 1
                value = each_line.replace(" ", "") \
                    .replace("string_value:", "") \
                    .replace("\"", "")

            if "number_value: " in each_line:
                counter += 1
                value = str(int(float(each_line.replace(" ", "") \
                                      .replace("number_value:", "") \
                                      .replace("\"", ""))))

            if counter == 2:
                end_result_parameters.append({
                    "key": key,
                    "value": value
                })
                counter = 0

        return end_result_parameters

    def get_df_field(self):
        return Process.__df_field.replace("Content",
                                          "<b>Query text:</b> {}".format(self.intent["query_text"]) + "<br>" +
                                          "<b>Detected intent:</b> {} (confidence: {})\n".format(
                                              self.intent["display_name"],
                                              self.intent["detection_confidence"],
                                          ) + "<br>" +
                                          "<b>Parameters: </b>" + str(
                                              self.__get_parameters_from_protobuf(str(self.params))
                                          )
                                          )

    @staticmethod
    def __generate_sql(view, filters):
        sql_select = ""
        sql_filters = ""

        if view == "Count something":
            sql_select = "SELECT COUNT(*) FROM SOMETABLE "
        if view == "Show something":
            sql_select = "SELECT * FROM SOMETABLE "

        if filters:
            sql_filters = "WHERE "
            for f in filters:
                if len(f["value"]) > 0:
                    sql_filters += f["key"] + " = " + f["value"] + " AND "

        if len(sql_filters) > 0:
            sql_filters = sql_filters[:-4] + ";"

        return sql_select + sql_filters

    def get_sql_field(self):
        return Process.__sql_field \
            .replace("Content",
                     self.__generate_sql(
                         self.intent["display_name"],
                         self.__get_parameters_from_protobuf(str(self.params))
                     )
                     )

    @staticmethod
    def filtering_dataframe(data, filters):
        pandas_filters = ""

        if filters:
            for f in filters:
                if len(f["value"]) > 0 and not f["value"].isnumeric():
                    pandas_filters += f["key"] + "==" + "\"" + f["value"] + "\"" + " & "

                elif len(f["value"]) > 0 and f["value"].isnumeric():
                    pandas_filters += f["key"] + "==" + f["value"] + " & "

        if len(pandas_filters) > 0:
            pandas_filters = pandas_filters[:-2]
        return data.query(pandas_filters)

    @staticmethod
    def human_readable_answer(data):
        count = len(data.index)
        return "There are {} people based on your parameters".format(count)

    def get_result_field(self, data):
        NO_PARAMS = True
        prms = self.__get_parameters_from_protobuf(str(self.params))
        for p in prms:
            if len(p["value"]) > 0:
                NO_PARAMS = False

        if self.intent["display_name"] == "Count something":
            if not NO_PARAMS:
                return \
                    Process.__result_field \
                        .replace("Content",
                                 str(self.human_readable_answer(self.filtering_dataframe(data,
                                                                                         self.__get_parameters_from_protobuf(
                                                                                             str(self.params)))))
                                 .replace("\n", "<br>")
                                 )
            else:
                return Process.__result_field \
                    .replace("Content", str(data).replace("\n", "<br>"))

        elif self.intent["display_name"] == "Show something":
            if not NO_PARAMS:
                return \
                    Process.__result_field \
                        .replace("Content",
                                 str(self.filtering_dataframe(data, self.__get_parameters_from_protobuf(
                                                                                             str(self.params))))
                                 .replace("\n", "<br>")
                                 )
            else:
                return Process.__result_field \
                    .replace("Content", str(data).replace("\n", "<br>"))

