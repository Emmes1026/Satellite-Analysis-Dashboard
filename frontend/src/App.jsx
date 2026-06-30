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

  async function handleSubmit(e) {
 
  const url = "http://localhost:8000";
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  setIsLoading(true);

  try {
    const response = await fetch(url, { method: "POST", body: formData })

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`)
    }

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

          <form className="w-fit mx-auto border-2 bg-slate-400 rounded-lg flex flex-row flex-wrap items-end mt-4 p-4 gap-4" onSubmit={handleSubmit}>

            <Field className="max-w-50">
              <FieldLabel htmlFor="input-field-image-name">
                Image name <span className="text-destructive">*</span>
              </FieldLabel>
              <Input name="image_name" id="input-field-image-name" type="text" placeholder="Enter image name" required/>
            </Field>

            <Field className="max-w-70">
              <FieldLabel htmlFor="input-field-image">
                Image <span className="text-destructive">*</span>
              </FieldLabel>
              <Input id="input-field-image" type="file" accept="image/*" required/>
            </Field>

            <Field className="max-w-20">
              <FieldLabel htmlFor="input-field-latitude">Latitude (optional)</FieldLabel>
              <Input id="input-field-latitude" type="number"/>
            </Field>

            <Field className="max-w-20">
              <FieldLabel htmlFor="input-field-longitude">Longitude (optional)</FieldLabel>
              <Input id="input-field-longitude" type="number"/>
            </Field>

            <Button type="submit" disabled={isLoading} >Submit</Button>

          </form>

          <div className="grow">

          </div>

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


