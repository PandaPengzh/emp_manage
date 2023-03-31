from django import forms

class BootstrapModelForm(forms.ModelForm):
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 添加样式：循环找到了所有的插件,如果有样式则是追加样式，如果没有则是添加了
        for name,field in self.fields.items():
            # 排除不需要添加样式的字段
            if name in self.bootstrap_exclude_fields:
                continue
            
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
         
            else:
                field.widget.attrs = {
                "class":"form-control",
                "placeholder":field.label
            }
