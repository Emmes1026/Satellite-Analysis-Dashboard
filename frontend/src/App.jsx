import './App.css'
import { useState } from 'react';
import { 
  Tabs, 
  TabsContent, 
  TabsList, 
  TabsTrigger 
} from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import {
  Field,
  FieldDescription,
  FieldLabel,
} from "@/components/ui/field"
import { Button } from "@/components/ui/button"



function App() {

  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)

  async function handleSubmit(e) {
 
  const url = "http://localhost:8000/api/images/";
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  setIsLoading(true);

  try {
    const response = await fetch(url, { method: "POST", body: formData })

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`)
    }
    let response_back = await response.json()
    setResult(response_back)

  } catch (error) {
    console.error(error.message);
  } finally {
    setIsLoading(false);
  }
}

  return (
    <div className="min-h-screen flex flex-col">
      <Tabs defaultValue="main" className="flex flex-col grow">

        <div className=" mx-auto border-2 bg-slate-400 rounded-lg flex place-content-center mt-6 p-2">
            <TabsList>
              <TabsTrigger value="main">Main Page</TabsTrigger>
              <TabsTrigger value="gallery">Gallery</TabsTrigger>
            </TabsList>
        </div>
        
        <TabsContent value="main" className="flex flex-col grow">

          <form className="w-3/4 mx-auto border-2 bg-slate-400 rounded-lg flex flex-row flex-wrap items-end place-content-center mt-4 p-4 gap-4" onSubmit={handleSubmit}>

            <Field className="max-w-50">
              <FieldLabel htmlFor="input-field-image-name">
                Image name <span className="text-destructive">*</span>
              </FieldLabel>
              <Input name="name" id="input-field-image-name" type="text" placeholder="Enter image name" required/>
            </Field>

            <Field className="max-w-70">
              <FieldLabel htmlFor="input-field-image">
                Image <span className="text-destructive">*</span>
              </FieldLabel>
              <Input name="image" id="input-field-image" type="file" accept="image/*" required/>
            </Field>

            <Field className="max-w-20">
              <FieldLabel htmlFor="input-field-latitude">Latitude (optional)</FieldLabel>
              <Input name="latitude" id="input-field-latitude" type="number" min="-90" max="90" step="any"/>
            </Field>

            <Field className="max-w-20">
              <FieldLabel htmlFor="input-field-longitude">Longitude (optional)</FieldLabel>
              <Input name="longitude" id="input-field-longitude" type="number" min="-180" max="180" step="any"/>
            </Field>

            <Button type="submit" disabled={isLoading} >Submit</Button>

          </form>

          {result && (
            <div className="w-3/4 mx-auto border-2 bg-slate-400 rounded-lg flex flex-col grow p-4 mt-6 items-center truncate">
              <h1 className="text-xl md:text-3xl font-bold tracking-tight">IMAGE OVERVIEW</h1>
              <p className="text-lg md:text-xl"> {result.name} </p>

              <img src={result.image} alt="Photo" className="max-w-full max-h-125 object-fit rounded-md"/>
            </div>
          )}


          <div className="flex">
          </div>          
        </TabsContent>

        <TabsContent value="gallery">

        </TabsContent>

      </Tabs>
    </div>

  )
}
export default App


