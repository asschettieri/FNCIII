from django.http import JsonResponse
from django.db.models import Q, F, CharField, Value, Func, Case, When, DateField, DateTimeField
import datetime

from django.utils import timezone

class Table:
    def __init__(self, request, queryset, fields, auto_columns=True, manual_name_and_verbose=None, additional_fields=None, table_filter=None, sortable=None, paginate=None):
        """
        
        Paramentri del costruttore - Obbligatori
        - request: contiene i dati della richiesta
        - queryset: contiene il queryset
        - fields: lista contenente i campi che si desidera prendere dal queryset
        
        Paramentri del costruttore - Opzionali
        - manual_name_and_verbose: dizionario contenente una tupla, dove il primo valore è il campo effettivo, e il secondo il valore leggibile (human readable).
          Nota: nel caso di annotazioni, è NECESSARIO impostare il manual_name_and_verbose
        - additional_fields: lista contenente i campi che si desidera aggiungere solo sulla struttura dati finale (ad esempio un eventuale id)
        - table_filter: contiene il valore ('global' o 'single') secondo il quale si decide se filtrare globalmente o singolarmente
        - sortable: valore booleano, per specificare se la tabella deve poter essere ordinata
        - paginate: valore booleano, per specificare se la tabella deve poter essere paginata
        
        """
        self.request = request
        self.draw = int(self.request.GET.get("draw", 0))
        self.start = int(self.request.GET.get("start", 0))
        self.length = int(self.request.GET.get("length", 10))
        self.search_value = self.request.GET.get("search[value]", "").strip()
        self.order_column_index = int(self.request.GET.get("order[0][column]", 0))
        self.order_direction = self.request.GET.get("order[0][dir]", "asc")
        self.queryset = queryset
        self.fields = fields
        self.manual_name_and_verbose = manual_name_and_verbose
        self.auto_columns = auto_columns
        if self.auto_columns:
            self.columns = self.create_columns()
        else:
            self.columns = []
        self.datatable_data_keys = [field for field in self.fields]
        self.table_columns_headers = [column[1] for column in self.columns]
        self.additional_fields = additional_fields
        self.table_filter = table_filter
        self.sortable = sortable
        self.paginate = paginate
        
    def create_columns(self):
        results = []
        def get_final_field(field):
            if '__' in field:
                new_fields = field.split('__')
                final_field = self.queryset.model._meta.get_field(new_fields[0])
                fields = [final_field]
                for x in range(1, len(new_fields)):
                    final_field = final_field.related_model._meta.get_field(new_fields[x])
                    fields.append(final_field)
                final_field = fields[-2] if fields[-2].__class__.__name__ == 'ForeignKey' else fields[-1]
            else:
                final_field = self.queryset.model._meta.get_field(field)
                
            results.append((final_field.name, final_field.verbose_name))
                        
        for field in self.fields:  
            if self.manual_name_and_verbose:
                if field not in self.manual_name_and_verbose:
                    get_final_field(field)
                else:
                    results.append(self.manual_name_and_verbose[field])
            else:
                get_final_field(field)
                    
        return results
    
    def filter_by_global_search(self):
        or_condition = Q()
        for field in self.fields:
            or_condition |= Q(**{f"{field}__icontains": self.search_value})     
        return self.queryset.filter(or_condition)
        
    def filter_by_single_search(self):
        and_condition = Q()
        for key, value in self.request.GET.items():
            if key.startswith('searchkey-') and value:
                field_name = key.replace('searchkey-', '')
                and_condition &= Q(**{f"{field_name}__icontains": value})
        return self.queryset.filter(and_condition)
        
    def sort(self):
        columns_and_orders = [value for key, value in self.request.GET.items() if key.startswith('order') and ('dir' in key or 'column' in key)]
        column_to_sort = []

        model_fields = {f.name: f for f in self.queryset.model._meta.get_fields()}

        for idx in range(0, len(columns_and_orders), 2):
            order_column = self.fields[int(columns_and_orders[idx])]
            order_direction = columns_and_orders[idx+1]

            original_field_name = order_column.replace('_formatted', '') if '_formatted' in order_column else order_column

            if original_field_name in model_fields and isinstance(model_fields[original_field_name], (DateField, DateTimeField)):
                order_column = original_field_name
            else:
                order_column = original_field_name

            if order_direction == "desc":
                order_column = "-" + order_column
            column_to_sort.append(order_column)
        return self.queryset.order_by(*column_to_sort)
        
    def count(self):
        return self.queryset.count()
        
    def paginate_queryset(self):
        return self.queryset[self.start : self.start + self.length]
    
    def make_response(self):
        if self.additional_fields:
            test_list = list(self.queryset.values(*self.datatable_data_keys + self.additional_fields))
        else:
            test_list = list(self.queryset.values(*self.datatable_data_keys))
            
        res_list = []
        for i in range(len(test_list)):
            if test_list[i] not in test_list[i + 1:]:
                res_list.append(test_list[i])
        return res_list
    
    def clean_results(self, results):
        for item in results:
            for chiave in item:
                item[chiave] = item[chiave] if item[chiave] is not None else ''
            
        return results
    
    def execute(self):
        
        if self.table_filter:
            if self.table_filter == 'global':
                if self.search_value:
                    self.queryset = self.filter_by_global_search()
            elif self.table_filter == 'single':
                self.queryset = self.filter_by_single_search()
                
        self.queryset = self.queryset.distinct()
                            
        if self.sortable:
            self.queryset = self.sort()
            
                    
        count = self.count()
        
        if self.paginate:
            self.queryset = self.paginate_queryset()
        
        data = self.make_response()
        
        data = self.clean_results(data)
        
        
        
        response = {
            "draw": self.draw,
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": data,
        }
        return JsonResponse(response)
    
class DjangoDataTable: #Nuova versione, per i prossimi progetti
    def __init__(self, request, queryset, fields, auto_columns=True, custom_verbose_names=None, additional_fields=None, filter_type=None, sort=None, paginate=None, none_values_replacement=''):
        """
        
        Paramentri del costruttore - Obbligatori
        - request: contiene tutti i dati della richiesta (sia i dati della GET che della POST, ma in questo caso verrà utilizzata solo la GET)
        - queryset: contiene il queryset
        - fields: lista contenente i campi che si desidera prendere dal queryset. Per accadere a chiavi esterne o relazioni estenre, usare id doppio underscore tra i campi (__)
        
        Paramentri del costruttore - Opzionali
        - custom_verbose_names: dizionario contenente come coppie chiave-valore i campi allegati ad un verbose name personalizzato.
          Nota: nel caso di annotazioni, è OBBLIGATORIO impostare il custom_verbose_names
        - additional_fields: lista contenente i campi che si desidera aggiungere solo sulla struttura dati finale, senza includerlo nella visualizzazione della tabella (ad esempio un eventuale id)
        - filter_type: contiene il valore ('global' o 'single') secondo il quale si decide se filtrare i dati globalmente o singolarmente
        - sort: valore booleano, per specificare se la tabella deve poter essere ordinata
        - paginate: valore booleano, per specificare se la tabella deve poter essere paginata
        
        """
        self.request = request
        self.draw = int(self.request.GET.get("draw", 0))
        self.start = int(self.request.GET.get("start", 0))
        self.length = int(self.request.GET.get("length", 10))
        self.search_value = self.request.GET.get("search[value]", "").strip()
        self.queryset = queryset
        self.fields = fields
        self.custom_verbose_names = custom_verbose_names
        self.auto_columns = auto_columns
        self.datatable_data_keys = [field for field in self.fields]
        if self.auto_columns:
            self.table_columns_headers = self.create_columns()
        else:
            self.table_columns_headers = []
        self.additional_fields = additional_fields
        self.filter_type = filter_type
        self.sort = sort
        self.paginate = paginate
        self.none_values_replacement = none_values_replacement
        
    def create_columns(self):
        results = []
        def get_final_field(field):
            if '__' in field:
                new_fields = field.split('__')
                final_field = self.queryset.model._meta.get_field(new_fields[0])
                fields = [final_field]
                for x in range(1, len(new_fields)):
                    final_field = final_field.related_model._meta.get_field(new_fields[x])
                    fields.append(final_field)
                final_field = fields[-2] if fields[-2].__class__.__name__ == 'ForeignKey' else fields[-1]
            else:
                final_field = self.queryset.model._meta.get_field(field)
                
            results.append(final_field.verbose_name)
                        
        for field in self.fields:  
            if self.custom_verbose_names:
                if field not in self.custom_verbose_names:
                    get_final_field(field)
                else:
                    results.append(self.custom_verbose_names[field])
            else:
                get_final_field(field)
                    
        return results
    
    def data_filtered_by_search(self, filter_type):
        if filter_type == 'global':
            or_condition = Q()
            for field in self.fields:
                or_condition |= Q(**{f"{field}__icontains": self.search_value})     
            return self.queryset.filter(or_condition)
        
        elif filter_type == 'single':
            and_condition = Q()
            for key, value in self.request.GET.items():
                if key.startswith('searchkey-') and value:
                    field_name = key.replace('searchkey-', '')
                    and_condition &= Q(**{f"{field_name}__icontains": value})
            return self.queryset.filter(and_condition)
            
        
    def sorted_data(self):
        columns_and_orders = [value for key, value in self.request.GET.items() if key.startswith('order') and ('dir' in key or 'column' in key)]
        column_to_sort = []
        for idx in range(0, len(columns_and_orders), 2):
            order_column = self.fields[int(columns_and_orders[idx])]
            order_direction = columns_and_orders[idx+1]
            if order_direction == "desc":
                order_column = "-" + order_column
            column_to_sort.append(order_column)
        return self.queryset.order_by(*column_to_sort)
        
    def paginated_data(self):
        return self.queryset[self.start : self.start + self.length]
    
    def converted_response(self):
        if self.additional_fields:
            test_list = list(self.queryset.values(*self.datatable_data_keys + self.additional_fields))
        else:
            test_list = list(self.queryset.values(*self.datatable_data_keys))
            
        res_list = []
        for i in range(len(test_list)):
            if test_list[i] not in test_list[i + 1:]:
                res_list.append(test_list[i])
        return res_list
    
    def replace_none_values(self, results, new_value):
        for item in results:
            for chiave in item:
                item[chiave] = item[chiave] if item[chiave] is not None else new_value
        return results
    
    def execute(self):
        if self.filter_type and self.search_value:
            self.queryset = self.data_filtered_by_search(self.filter_type)
                            
        if self.sort:
            self.queryset = self.sorted_data()
            
        self.queryset = self.queryset.distinct()
                    
        count = self.queryset.count()
        
        if self.paginate:
            self.queryset = self.paginated_data()
        
        data = self.converted_response()
        
        data = self.replace_none_values(data, self.none_values_replacement)
        
        response = {
            "draw": self.draw,
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": data,
        }
        return JsonResponse(response)

class Table2(Table):
    def make_response(self):
        if self.additional_fields:
            results = list(self.queryset.values(*self.datatable_data_keys + self.additional_fields))
        else:
            results = list(self.queryset.values(*self.datatable_data_keys))
        
        return results
    
    def remove_duplicates(self, results):
        new_results = []
        for i in range(len(results)):
            if results[i] not in results[i+1:]:
                new_results.append(results[i])
        return new_results
    
    def clean_and_format_results(self, results):
        for i in range(len(results)):
            for key, value in results[i].items():
                results[i][key] = value if value is not None else ''
                if isinstance(value, datetime.date) and value != '':
                    results[i][key] = results[i][key].strftime("%d/%m/%Y")
        return results
     
    def count(self, data):
        return len(data)
    
    def search_filter(self, data):
        return [item for item in data if any(self.search_value.lower() in str(value).lower() for value in item.values())]

    def sort(self, data):
        order_column = self.fields[self.order_column_index]
        key = lambda x: str(x[order_column]).lower()
        return sorted(data, key=key, reverse=self.order_direction == "desc")
        
    def paginate_data(self, data):
        return data[self.start : self.start + self.length]
    
    def execute(self):
        self.queryset = self.queryset.distinct()
        
        data = self.make_response()
        
        data = self.remove_duplicates(data)
        
        data = self.clean_and_format_results(data)
                
        if self.search_value:
            data = self.search_filter(data)
            
        count = self.count(data)
                        
        if self.sortable:
            data = self.sort(data)
        
        if self.paginate:
            data = self.paginate_data(data)
                    
        response = {
            "draw": self.draw,
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": data,
        }
        return JsonResponse(response)

def convert_date(field):
    formatted_date = Func(
            F(field),
            Value('%d/%m/%Y'), 
            function='DATE_FORMAT',
            output_field=CharField()
        )
    return formatted_date

def convert_datetime(field):
    formatted_datetime = Func(
            F(field),
            Value('%d/%m/%Y %H:%i:%s'), 
            function='DATE_FORMAT',
            output_field=CharField()
        )
    return formatted_datetime

def convert_0_1_to_verbose(field_name):
    positive_condition = Q(**{field_name: 1})
    negative_condition = Q(**{field_name: 0})
    
    formatted_value = Case(
        When(positive_condition, then=Value("Si")),
        When(negative_condition, then=Value("No")),
        default=Value(""),
        output_field=CharField()
    )
    return formatted_value