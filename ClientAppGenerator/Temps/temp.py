def update_action_component_creator(list_table_configs, list_column_configs, list_foreign_key_config, client_api_package_name, dbinfo):
    update_component_path = './ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-update-ui-component'
    update_component_filename = './ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-update-ui-component/{0}-update-ui.component.{1}'
    update_html_template_path = './TemplateFiles/ActionTemplate/update-ui/update-ui.component.html'
    update_scss_template_path = './TemplateFiles/ActionTemplate/update-ui/update-ui.component.scss'
    update_ts_template_path = './TemplateFiles/ActionTemplate/update-ui/update-ui.component.ts'
    update_html_data_field_template_path = './TemplateFiles/ActionTemplate/update-ui/html_data_field_template.txt'
    ddl_html_component_template = './TemplateFiles/HtmlComponent/DropDownList.txt'
    import_list = []
    declare_list = []
    path_list = []
    
    html_data_field_template = ''
    with open(update_html_data_field_template_path, 'r') as r1:
        html_data_field_template = ''.join(r1.readlines())
        r1.close()
        
    html_ddl_field_template = ''
    with open(ddl_html_component_template, 'r') as r2:
        html_ddl_field_template = ''.join(r2.readlines())
        r2.close()
        
    list_table_configs = [w for w in list_table_configs if 'C' in w.ActionGroup]
    
    for table_config in list_table_configs:
        modelName = table_config.ModelName
        serviceName = modelName + 'Service'
        explicitName = table_config.ExplicitName
        tableUiComponentPath = '{0}-table-ui/{0}-table-ui.component'.format(modelName.lower())
        updateClassName = modelName + 'updateUIComponent'
        selectorName = 'app-{0}-update-ui-component'.format(modelName.lower())
        urlName = '{0}-update-ui.component'.format(modelName.lower()) 
        belonged_fk = [w for w in list_foreign_key_config if w.SourceTableName == table_config.Name]
                    
        import_item = [updateClassName, './components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-update-ui-component/{0}-update-ui.component'.format(table_config.ModelName.lower())]
        path_item = "      { path: 'index/0/update', component: updateUIComponent },\n".replace('updateUIComponent', updateClassName).replace('0', modelName.lower() + 'management')
        import_list.append(import_item)
        declare_list.append(updateClassName)
        path_list.append(path_item)

        
        belonged_colum_config = [column_config for column_config in list_column_configs if column_config.TableId == table_config.Id]
        belonged_colum_config = sorted(list(belonged_colum_config),
                                       key=lambda x: x.OrdinalPosition)
        
        html_insert = ''
        primary_key_column = [x for x in belonged_colum_config if x.IsPrimaryKey]
        input_component_idx = -1
        data_field = '\n'
        for column_config in belonged_colum_config:
            if not (column_config.IsPrimaryKey == 1 and column_config.IsAutoIncremental == 1):
                input_component_idx += 1
                if input_component_idx % 2 == 0:
                    data_field += '      <div class="row" style="margin-bottom: 30px">\n'
                    
                if not column_config.IsForeignKey:
                    data_field += html_data_field_template.replace('[--DisplayName--]', column_config.ExplicitName) .replace('[--ModelNameWithLower--]', column_config.PropertyName[0].lower() + column_config.PropertyName[1:]).replace('[--DisableIfPrimaryKey--]', 'disabled' if column_config.IsPrimaryKey else '') +'\n'
                else:
                    fk_refrenced_info = [w for w in belonged_fk if w.SourceColumnName == column_config.ColumnName][0]
                    fk_table_refrenced_info = [w for w in list_table_configs if w.Name == fk_refrenced_info.RefrencedTableName][0]
                    column_property_name = column_config.PropertyName
                    column_property_name_lower_first = column_config.PropertyName[0].lower() + column_config.PropertyName[1:]
                    table_model_name_lower_first = fk_table_refrenced_info.ModelName[0].lower() + fk_table_refrenced_info.ModelName[1:]
                    fk_items = table_model_name_lower_first + 'Items'
                    refrenced_column_name = [w.PropertyName for w in list_column_configs if w.ColumnName == fk_refrenced_info.RefrencedColumnName and w.TableId == fk_table_refrenced_info.Id][0]
                    mapped_refrenced_column_name = [w.PropertyName for w in list_column_configs if w.ColumnName == fk_refrenced_info.MappedRefrencedColumnName and w.TableId == fk_table_refrenced_info.Id][0]
                    data_field += html_ddl_field_template.replace('[--ColumnPropertyName--]', column_property_name) \
                                                         .replace('[--ColumnPropertyNameLowerFirst--]', column_property_name_lower_first).replace('[--FKItems--]', fk_items)  \
                                                         .replace('[--RefrencedColumnNameLowerFirst--]', refrenced_column_name[0].lower() + refrenced_column_name[1:]) \
                                                         .replace('[--MappedRefrencedColumnNameLowerFirst--]', mapped_refrenced_column_name[0].lower() + mapped_refrenced_column_name[1:]) \
                                                         .replace('[--DisplayName--]', column_config.ExplicitName)
                if input_component_idx % 2 == 1 or input_component_idx >= len(belonged_colum_config):
                    data_field += '      </div>\n'
                    html_insert += data_field
                    data_field = '\n'

            
        # create update action
        os.makedirs(update_component_path.format(table_config.ModelName.lower()))
        
        # create html file
        with open(update_html_template_path, 'r') as r_html:
            html_contents = r_html.readlines()
            modified_html_contents = []
            for line in html_contents:
                if '[--InsertHere--]' in line:
                    line = html_insert
                if '[--ExceplitName--]' in line:
                    line = line.replace('[--ExceplitName--]', table_config.ExplicitName)
                if '[--LowerModelName--]' in line:
                    line = line.replace('[--LowerModelName--]', modelName.lower())
                modified_html_contents.append(line)
            r_html.close()
        with open(update_component_filename.format(table_config.ModelName.lower(), 'html'), 'w') as w_html:
            w_html.write(''.join(modified_html_contents))
            w_html.close()  
        
        # create style file
        copyfile(update_scss_template_path, update_component_filename.format(table_config.ModelName.lower(), 'scss'))
        
        fk_service_list = ''
        fk_model_list = ''
        fk_items = ''
        fk_services = ''
        inject_fk = ''
        fk_service_set_auth = ''
        fk_service_init = ''
        fk_item_init = ''
        fk_data_binding = ''
        
        for fk_config in belonged_fk:
            refrenced_table_details = [w for w in list_table_configs if w.Name == fk_config.RefrencedTableName][0]
            # refrenced_column_details = [w for w in list_column_configs if w.ColumnName == fk_config.RefrencedColumnName and w.TableId == refrenced_table_details.Id][0]
            property_name = refrenced_table_details.ModelName
            property_name_first_lower = refrenced_table_details.ModelName[0].lower() + refrenced_table_details.ModelName[1:]
            
            if fk_config.RefrencedTableName != table_config.Name:
                fk_service_list += property_name + 'Service, '
                fk_model_list += property_name + ', '
            fk_items += '  ' + property_name_first_lower + 'Items: ' + property_name + '[] = [];\n'
            fk_services += '  ' +  property_name_first_lower + 'Service: ' + property_name + 'Service;\n'
            inject_fk += '    @Inject({0}Service) {1}srv:  {0}Service,\n'.format(property_name, property_name_first_lower)
            fk_service_set_auth += '    ' + property_name_first_lower + 'srv.defaultHeaders = new HttpHeaders({\n' \
                                   '      "Content-Type": "application/json",\n' \
                                   '      Authorization: "Bearer " + this.token,\n' \
                                   '    });\n'
            fk_service_init += '    this.{0}Service = {0}srv;\n'.format(property_name_first_lower)
            fk_item_init += '    this.{0}Items = {2} as {1}\n'.format(property_name_first_lower, property_name, '{}')
            
            fk_data_binding += '    this.' + property_name_first_lower + 'Service.api' + property_name + 'Get().subscribe((result) => {\n' \
                               '      this.' + property_name_first_lower + 'Items = result;\n' \
                               '    })\n' 
        # update ts file
        with open(update_ts_template_path, 'r') as r_ts:
            ts_contents = r_ts.readlines()
            modified_ts_contents = []
            for line in ts_contents:
                if '[--TableUIComponentPath--]' in line:
                    line = line.replace('[--TableUIComponentPath--]', tableUiComponentPath)
                if '[--ServiceName--]' in line:
                    line = line.replace('[--ServiceName--]', serviceName)
                if '[--SelectorName--]' in line:
                    line = line.replace('[--SelectorName--]', selectorName)
                if '[--UrlName--]' in line:
                    line = line.replace('[--UrlName--]', urlName)
                if '[--ClassName--]' in line:
                    line = line.replace('[--ClassName--]', updateClassName)
                if '[--ApiClientPackageId--]' in line:
                    line = line.replace('[--ApiClientPackageId--]', client_api_package_name)
                if '[--ModelName--]' in line:
                    line = line.replace('[--ModelName--]', modelName)
                if '[--CastedIdSelectInput--]' in line:
                    data_type = db_to_net_data_type_convert(primary_key_column[0].DataType)
                    if data_type == 'string':
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInput')
                    else:
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInputNumber')
                if '[--FKServiceName--]' in line:
                    line = line.replace('[--FKServiceName--]', fk_service_list)
                if '[--FKModelName--]' in line:
                    line = line.replace('[--FKModelName--]', fk_model_list)
                if '[--FKItems--]' in line:
                    line = line.replace('[--FKItems--]', fk_items)
                if '[--FKServices--]' in line:
                    line = line.replace('[--FKServices--]', fk_services)
                if '[--InjectFK--]' in line:
                    line = line.replace('[--InjectFK--]', inject_fk)
                if '[--FKServiceSetAuth--]' in line:
                    line = line.replace('[--FKServiceSetAuth--]', fk_service_set_auth)
                if '[---FKItemsInit--]' in line:
                    line = line.replace('[---FKItemsInit--]', fk_item_init)
                if '[---FKServiceInit--]' in line:
                    line = line.replace('[---FKServiceInit--]', fk_service_init)
                if '[--FKDataBinding--]' in line:
                    line = line.replace('[--FKDataBinding--]', fk_data_binding)
                if '[--ExplicitName--]' in line:
                    line = line.replace('[--ExplicitName--]', explicitName)
                if '[--LowerModelName--]' in line:
                    line = line.replace('[--LowerModelName--]', modelName.lower())
                if '[--CastedIdSelectInput--]' in line:
                    data_type = db_to_net_data_type_convert(primary_key_column[0].DataType)
                    if data_type == 'string':
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInput')
                    else:
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInputNumber')
                modified_ts_contents.append(line)
            r_ts.close()
        with open(update_component_filename.format(table_config.ModelName.lower(), 'ts'), 'w') as w:
            w.write(''.join(modified_ts_contents))
            w.close()  
    update_app_module_file_for_action(import_list, declare_list)
    update_routing_file_for_action(import_list, path_list)