# Template tags

Template tags (also known as **template variables**) are a way for you to substitute data into your workflow at runtime. Template tags are delimited by `{{` and `}}` and will be replaced when the template is executed.

What tags are available to use depends on the template type, and there are a number of global ones you can use, such as `{{workflow.name}}`, which is replaced by the workflow's name:

```yaml
    - name: main
      container:
        image: docker/whalesay
        command: [ cowsay ]
        args: [ "hello {{workflow.name}}" ]
```

Look at the full example:

```bash
cat template-tag-workflow.yaml
```

Submit this workflow:

```bash
argo submit --watch template-tag-workflow.yaml
```

You can see the output by running

```bash
argo logs @latest
```

You should see something like:

```output
 __________________________
< hello template-tag-kqpc6 >
 --------------------------
    \
     \
      \     
                    ##        .            
              ## ## ##       ==            
           ## ## ## ##      ===            
       /""""""""""""""""___/ ===        
  ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~   
       \______ o          __/            
        \    \        __/             
          \____\______/   
```

There are many more different tags, you can [read more about template tags in the docs](https://argoproj.github.io/argo-workflows/variables/).

# Exercise

Change the workflow to echo the date the workflow was created.

## Solution
```yaml                                           
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: template-tag-
spec:
  entrypoint: main
  templates:
    - name: main
      container:
        image: docker/whalesay
        command: [ cowsay ]
        args: [ "hello {{workflow.name}} created on {{workflow.creationTimestamp}}" ]
```
Expected output:
```output
template-tag-kbzgk:  _____________________________________ 
template-tag-kbzgk: / hello template-tag-kbzgk created on \
template-tag-kbzgk: \ 2023-02-04T22:48:52Z                /
template-tag-kbzgk:  ------------------------------------- 
template-tag-kbzgk:     \
template-tag-kbzgk:      \
template-tag-kbzgk:       \     
template-tag-kbzgk:                     ##        .            
template-tag-kbzgk:               ## ## ##       ==            
template-tag-kbzgk:            ## ## ## ##      ===            
template-tag-kbzgk:        /""""""""""""""""___/ ===        
template-tag-kbzgk:   ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~   
template-tag-kbzgk:        \______ o          __/            
template-tag-kbzgk:         \    \        __/             
template-tag-kbzgk:           \____\______/   
template-tag-kbzgk: time="2023-02-04T22:48:55.828Z" level=info msg="sub-process exited" argo=true error="<nil>"
```

